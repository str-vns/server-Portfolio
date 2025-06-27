from rest_framework import authentication
from .firebase_exceptions import (
    FirebaseAuthentication,
    NoAuthToken,
    InvalidAuthToken,
    FirebaseError,
    EmailVerification,
)
from firebase_admin import auth, credentials
import firebase_admin
from django.db import IntegrityError
import os

try:
    cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS_PATH"))
    default_app = firebase_admin.initialize_app(cred)
except Exception:
    raise FirebaseError(
        "Firebase configuration credentials are not set properly. Please check your environment variables."
    )

class FirebaseAuthentication(authentication.BaseAuthentication):
    keyword = 'Bearer'
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise NoAuthToken("Authentication token is required.")
        id_token = auth_header.split(' ').pop()
        decoded_token = None
        
        try: 
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid authentication token.")
        if not id_token or not decoded_token:
            return None
        email_verified = decoded_token.get('email_verified', False)
        if not email_verified:
            raise EmailVerification("Email verification is required to access this resource.")
        try:
           uid = decoded_token.get('uid')
        except Exception:
            raise FirebaseError("An error occurred while authenticating with Firebase. Please try again later.")
        try: 
          user, _= DriveUser.objects.get_or_create(
            firebase_uid=uid,
            defauts={
                "first_name": decoded_token.get('name', ''),
                 "phone_number": decoded_token.get('phone_number', ''),
            }
          )
        except IntegrityError as e:
            raise FirebaseError("An error occurred while creating the user. Please try again later.")
        except Exception as e:
            raise FirebaseError(f"An error occurred while creating the user: {str(e)}")
        return (user, None)
        
from rest_framework.exceptions import APIException
from rest_framework import status

class NoAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Authentication token is required."
    default_code = "no_auth_token"

class InvalidAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid authentication token."
    default_code = "invalid_auth_token"
    
class FirebaseAuthError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = "firebase_auth_error"
    default_detail = "An error occurred while authenticating with Firebase. Please try again later."
    
class EmailVerification(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Email verification is required to access this resource."
    default_code = "email_verification_required"
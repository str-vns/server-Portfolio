from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ...models import User
from ...serializers import UserSerializer
from ...utils.Firebase.firebase_authentication import auth as firebase_auth
from ...utils.email_verification import generate_custom_email_from_firebase
import re
from drf_with_firebase.settings import auth

class AuthCreateNewUserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    @swagger_auto_schema(
        operation_summary="Create a new user",
        tags=["User Management"],
        request_body=UserSerializer,
        responses={
            201: UserSerializer(many=False),
            400: "User creation failed. Please check the provided data.",
        }
    )
    def post(self, request, format=None):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        included_fields = [ email, password, first_name, last_name ]
        
        if not all(included_fields):
            bad_response = {
                "status" : "Failed",
                "message": "All fields are required."
            }
            
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            bad_response = {
                "status" : "Failed",
                "message": "Invalid email format."
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 8 : 
            bad_response = {
                "status" : "Failed",
                "message": "Password must be at least 8 characters long."
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        if password is not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"):
            bad_response = {
                "status" : "Failed",
                "message": "Password must contain at least one letter and one number."
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = auth.create_user_with_email_and_password(email, password)
            uid = user['localId']
            data['firebase_uid'] = uid
            data["is_active"] = True
            
            try:
                user_email = email
                display_name = first_name.capitalize() + " " + last_name.capitalize()
                generate_custom_email_from_firebase(
                    user_email=user_email,
                    display_name=display_name,
                    firebase_uid=uid
                )
            except Exception as e:
                firebase_admin_auth.delete_user(uid)
                bad_response = {
                    "status": "Failed",
                    "message": f"Failed to send email verification: {str(e)}"
                }
                return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "Success",
                    "message": "User created successfully.",
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                auth.delete_user_account(user['idToken'])
                bad_response = {
                    "status": "Failed",
                    "message": "User creation failed. Please check the provided data.",
                    "errors": serializer.errors
                }
                return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            bad_response = {
                "status": "Failed",
                "message": f"An error occurred while creating the user: {str(e)}"
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        
class AuthLoginExistingUserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    @swagger_auto_schema(
        operation_summary="Login an existing user",
        operation_description="Login an existing user with email and password.",
        tags=["User Management"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password')
            },
        )
        responses={
            200: UserSerializer(many=False),
            400: "User does not exist or password is incorrect.",
        }
    )
    def post(self, request: Request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            bad_response = {
                "status": "Failed",
                "message": f"An error occurred while logging in: {str(e)}"
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        try:
            isExistingUser = User.objects.get(email=email)
            if not check_password(password, isExistingUser.password):
                isExistingUser.set_password(password)
                isExistingUser.save()
            serializer = UserSerializer(isExistingUser)
            extra_data = {
                'firebase_uid': user['localId'],
                'firebase_access_token': user['idToken'],
                'firebase_refresh_token': user['refreshToken'],
                'firebase_expires_in': user['expiresIn'],
                'firebase_kind': user['kind'],
                'user_data': serializer.data
            }
            response = {
                "status": "Success",
                "message": "User logged in successfully.",
                "data": extra_data
            }
            return Response(response, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            auth.delete_user_account(user['idToken'])
            bad_response = {
                "status": "Failed",
                "message": "User does not exist or password is incorrect."
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
    
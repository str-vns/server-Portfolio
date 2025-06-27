import os
import pyrebase
from decouple import config as env_config

SECRET_KEY = env_config("SECRET_KEY")


def initialize_firebase_app():
    try:
        firebase_config = {
            "apiKey": os.getenv("FIREBASE_API_KEY"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
            "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        }

        firebase = pyrebase.initializa_app(firebase_config)
        auth = firebase.auth()
    except Exception as Error:
        raise Error(
            "Firebase configuration credentials are not set properly. Please check your environment variables."
        )

    AUTH_USER_MODEL = "accounts.user"
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "accounts.firebase_auth.firebase_authentication.FirebaseAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ],
    }

    AUTHENTICATION_BACKEND = [
        "accounts.backends.models_backend.ModelsBackend",
    ]
    
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env_config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env_config("EMAIL_HOST_PASSWORD")
    
    
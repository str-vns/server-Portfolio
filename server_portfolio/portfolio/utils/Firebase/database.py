from django.shortcuts import render
import pyrebase
from decouple import config as env_config
import firebase_admin 
from firebase_admin import credentials, storage
import os

firebaseConfig = {
    "apiKey": env_config("FIREBASE_API_KEY"),
    "authDomain": env_config("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": env_config("FIREBASE_DATABASE_URL"),
    "projectId": env_config("FIREBASE_PROJECT_ID"),
    "storageBucket": env_config("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": env_config("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": env_config("FIREBASE_API_ID"),
    # "measurementId": env_config("FIREBASE_MEASUREMENT_ID"),
}

googleCred = {
  "type": env_config("GOOGLE_TYPE"),
  "project_id": env_config("GOOGLE_PROJECT_ID"),
  "private_key_id": env_config("GOOGLE_PRIVATE_KEY_ID"),
  "private_key": env_config("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
  "client_email": env_config("GOOGLE_CLIENT_EMAIL"),
  "client_id": env_config("GOOGLE_CLIENT_ID"),
  "auth_uri": env_config("GOOGLE_AUTH_URI"),
  "token_uri": env_config("GOOGLE_TOKEN_URI"),
  "auth_provider_x509_cert_url": env_config("GOOGLE_AUTH_PROVIDER"),
  "client_x509_cert_url": env_config("GOOGLE_CLIENT"),
  "universe_domain": env_config("GOOGLE_UNIVERSE_DOMAIN")
}

cred = credentials.Certificate(googleCred)
firebase_admin.initialize_app(cred, {
    'storageBucket': env_config("FIREBASE_STORAGE_BUCKET")
})

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
database = firebase.database()
storageFire = firebase.storage()
storage = storage.bucket()

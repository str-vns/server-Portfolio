from portfolio.utils.Firebase.database import firebase
from decouple import config as env_config

auth = firebase.auth()
user = auth.sign_in_with_email_and_password(env_config("FIREBASE_USER"), env_config("FIREBASE_PASSWORD"))
token = user['idToken']

from accounts.firebase_auth.firebase_authentication import auth as firebase_auth
from django.core.mail import send_mail
from django.conf import settings

def generate_custom_email_from_firebase(user_email, display_name):
    action_code_settings = firebase_auth.ActionCodeSettings(
        url='https://www.yourwebsite.example/',
        handle_code_in_app=True,
    )
    custom_verification_link = firebase_auth.generate_email_verification_link(user_email, action_code_settings)
    subject = 'Verify your email address'
    message = f'Hello {display_name},\n\nPlease verify your email address by clicking on the link below:\n\n{custom_verification_link}\n\nThanks,\nYour website team'
    send_email(subject, message, user_email)

    def send_email(subject, message, user_email):
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [user_email])
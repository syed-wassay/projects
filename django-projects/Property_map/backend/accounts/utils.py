from django.core.mail import EmailMessage
import os
from dotenv import load_dotenv
import threading

load_dotenv()


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], 
            body=data['email_body'],
            from_email=os.getenv('EMAIL_HOST_USER'),
            to=[data['to_email']])
        EmailThread(email).start()
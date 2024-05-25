from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP
from decouple import config
from models.models import EmailSchema
from fastapi import HTTPException

HOST = config("MAIL_HOST")
USERNAME = config("MAIL_USERNAME")
PASSWORD = config("MAIL_PASSWORD")
PORT = config("MAIL_PORT")
TIMEOUT = 20

def send_mail(data: dict | None = None):
    print("here")
    message = MIMEText(data['body'])
    message['Subject'] = data['subject']
    message['From'] = 'no-reply@example.com'
    message['To'] = ', '.join(data['email'])

    # ctx = create_default_context()

    try:
        server = SMTP(HOST, PORT, timeout=TIMEOUT)
        server.sendmail(message["From"], message["To"] , message.as_string())
        server.close()

        print('Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
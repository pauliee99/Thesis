from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP
from decouple import config
from models.models import EmailSchema

HOST = config("MAIL_HOST")
USERNAME = config("MAIL_USERNAME")
PASSWORD = config("MAIL_PASSWORD")
PORT = config("MAIL_PORT")

def send_mail(data: dict | None = None):
    msg = EmailSchema(**data)
    message = MIMEText(msg.body, "html")
    message["From"] = USERNAME
    message["To"] = ",".join(msg.email)
    message["Subject"] = msg.subject

    ctx = create_default_context()

    try:
        with SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(USERNAME, PASSWORD)
            server.send_message(message)
            server.quit()
        return {"status": 200, "errors": None}
    except Exception as e:
        return {"status": 500, "errors": e}
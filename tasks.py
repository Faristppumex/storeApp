from celery_worker import celery
import smtplib
from email.mime.text import MIMEText
import os

def send_email_task(to_email, subject, body):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [to_email], msg.as_string())

@celery.task
def send_email(request):
    print(f"data: {request}")
    send_email_task(
        to_email=request.get('email'),
        subject=request.get('subject', 'user request'),
        body=request.get('body', f"User created with email: {request.get('email')}, name: {request.get('name')}, role: {request.get('role')}")
    )
    print(f"Sending email for {request.get('email')}")
    return "sending email"


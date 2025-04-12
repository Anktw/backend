import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

def send_reset_email(email_to: str, reset_token: str):
    reset_link = f"http://localhost:3000/reset-password?token={reset_token}"  # Update for frontend
    subject = "Password Reset Request"
    body = f"""\
Hi,

You requested a password reset. Click the link below to reset your password:

{reset_link}

If you did not request this, please ignore this email.
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = email_to

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, email_to, msg.as_string())

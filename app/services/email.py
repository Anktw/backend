import smtplib
from email.mime.text import MIMEText
from app.core.config import settings


def send_email(email_to: str, subject: str, body: str):
    msg=MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = email_to
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, email_to, msg.as_string())


#Reset Password Email
def send_reset_email(email_to: str, reset_token: str):
    reset_link = f"http://localhost:3000/reset-password?token={reset_token}"  # Update for frontend
    subject = "Password Reset Request"
    body = f"""\
Hi,

You requested a password reset. Click the link below to reset your password:

{reset_link}

If you did not request this, please ignore this email.
"""
    send_email(email_to, subject, body)


#Registration OTP Email
def send_registration_email(email_to: str, otp: str):
    verify_link = f"http://localhost:3000/verify-otp?email={email_to}"
    subject = "Verify Your Email Address"
    body = f"""\
Hi,

Thanks for registering! Please verify your email address using the OTP below:

OTP: {otp}

Or click the link to verify your account:
{verify_link}

This helps us confirm your identity and complete your signup.
"""
    send_email(email_to, subject, body)


#Account Created Email
def send_account_created_email(email_to: str):
    subject = "Account Created Successfully"
    body = f"""\
Hi,

Your account has been successfully verified and created 🎉

You can now log in and start using the app!

Thanks for joining us!
"""
    send_email(email_to, subject, body)
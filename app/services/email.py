from email import message
from email.utils import formataddr
import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

sender_name = "unkit.site"
sender_email = settings.SMTP_USER

def send_email(email_to: str, subject: str, body: str):
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = email_to
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, email_to, msg.as_string())


#Registration OTP Email
def send_registration_email(email_to: str, otp: str):
    subject = "Verify Your Email Address"
    body = f"""<body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 40px; color: #333;">
  <table style="max-width: 600px; margin: auto; background: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
    <tr>
      <td style="text-align: center; font-size: 24px; font-weight: bold; padding-bottom: 20px; color: #222;">
        Verify Your Email
      </td>
    </tr>
    <tr>
      <td style="font-size: 16px; line-height: 1.6; color: #555;">
        Hi,<br><br>
        Please verify your email address using the OTP below:
      </td>
    </tr>
    <tr>
      <td style="text-align: center; font-size: 28px; font-weight: bold; color: #222; padding: 20px 0;">
        {otp}
      </td>
    </tr>
    <tr>
      <td style="font-size: 14px; line-height: 1.6; color: #999; text-align: center; padding-top: 20px;">
        This helps me to confirm your identity and complete your signup.
      </td>
    </tr>
  </table>
</body>
"""
    send_email(email_to, subject, body)


#Account Created Email
def send_account_created_email(email_to: str):
    subject = "Account Created Successfully"
    body = f"""\
<body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 40px; color: #333;">
  <table style="max-width: 600px; margin: auto; background: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
    <tr>
      <td style="text-align: center; font-size: 24px; font-weight: bold; padding-bottom: 20px; color: #222;">
        Welcome Aboard!
      </td>
    </tr>
    <tr>
      <td style="font-size: 16px; line-height: 1.6; color: #555;">
        Hi,<br><br>
        Your account has been successfully verified and created...<br><br>
        You can now log in and start using the app!
      </td>
    </tr>
    <tr>
      <td style="font-size: 14px; line-height: 1.6; color: #999; text-align: center; padding-top: 20px;">
        Thanks for joining me!
      </td>
    </tr>
  </table>
</body>
"""
    send_email(email_to, subject, body)


#Reset Password Email
def send_reset_email(email_to: str, otp: str):
    subject = "Password Reset Request"
    body = f"""\
<body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 40px; color: #333;">
  <table style="max-width: 600px; margin: auto; background: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
    <tr>
      <td style="text-align: center; font-size: 24px; font-weight: bold; padding-bottom: 20px; color: #222;">
        Password Reset Request
      </td>
    </tr>
    <tr>
      <td style="font-size: 16px; line-height: 1.6; color: #555;">
        Hi,<br><br>
        You requested a password reset. Enter the OTP in the app to reset your password:
        <tr>
            <td style="text-align: center; font-size: 28px; font-weight: bold; color: #222; padding: 20px 0;">
                {otp}
            </td>
      </td>
    </tr>
    <tr>
      <td style="font-size: 14px; line-height: 1.6; color: #999; text-align: center; padding-top: 20px;">
        If you did not request this, please ignore this email.
      </td>
    </tr>
  </table>
</body>
"""
    send_email(email_to, subject, body)


#Password Changed Email
def send_password_changed_email(email_to: str):
    subject = "Password Changed Successfully"
    body = f"""\
<body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 40px; color: #333;">
  <table style="max-width: 600px; margin: auto; background: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
    <tr>
      <td style="text-align: center; font-size: 24px; font-weight: bold; padding-bottom: 20px; color: #222;">
        Welcome Aboard!
      </td>
    </tr>
    <tr>
      <td style="font-size: 16px; line-height: 1.6; color: #555;">
        Hi,<br><br>
        Your password has been successfully updated 🎉<br><br>
        You can now log in and start using the app!
      </td>
    </tr>
    <tr>
      <td style="font-size: 14px; line-height: 1.6; color: #999; text-align: center; padding-top: 20px;">
        Thanks for joining me!
      </td>
    </tr>
  </table>
</body>
"""
    send_email(email_to, subject, body)
import smtplib
import os
from email.message import EmailMessage

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
print("SMTP_EMAIL:", SMTP_EMAIL)
print("SMTP_PASSWORD:", "SET" if SMTP_PASSWORD else "MISSING")

def send_magic_link(to_email: str, link: str):
    msg = EmailMessage()
    msg["Subject"] = "Sub Rosa Login Link"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg.set_content(f"""
Click the link below to log in to Sub Rosa.
This link expires in 5 minutes.

{link}
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)


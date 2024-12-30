# app/core/utils.py

from typing import Optional
from fastapi import HTTPException
from app.core.config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
from smtplib import SMTPException as SMTPError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Utility function to send emails
def send_email(to_email: str, subject: str, body: str, from_email: Optional[str] = SMTP_USER):
    # Create the message
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Try to send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SMTP_USER, SMTP_PASSWORD)  # Log in to the email server
        server.sendmail(from_email, to_email, msg.as_string())  # Send email
        server.quit()  # Disconnect from the server
    except SMTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email. SMTP error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email. Error: {str(e)}"
        )

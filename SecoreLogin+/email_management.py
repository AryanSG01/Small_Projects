import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_username"
SMTP_PASSWORD = "your_password"
SENDER_EMAIL = "your_email@example.com"

# Function to send a password reset email
def send_password_reset_email(email, new_password):
    # Create a multipart email message
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = email
    message["Subject"] = "Password Reset"

    # Create the plain text part of the message
    text = f"Your new password is: {new_password}"

    # Attach the plain text message to the email
    message.attach(MIMEText(text, "plain"))

    # Connect to the SMTP server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    
    # Send the email
    server.send_message(message)

    # Disconnect from the SMTP server
    server.quit()

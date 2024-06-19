import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

def send_email_alert(sub,mess, t, receiver):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_PASSWORD")

    from_email = 'thewizard3693@gmail.com'
    to_email = receiver
    subject = sub
    body = f'This is to inform that at {t} the following integrity was compromised. Please do check and take action accordingly'
    body += "\n"+mess
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')

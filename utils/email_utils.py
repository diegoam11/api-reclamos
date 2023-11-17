# email_utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject, body, to_email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "correodesde@gmail.com"
    smtp_password = "clave"

    message = MIMEMultipart()
    message["From"] = smtp_username
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_username, smtp_password)

            server.sendmail(smtp_username, to_email, message.as_string())

        print("Correo electrónico enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {str(e)}")

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from core.config import settings

def send_email(to_email: str, subject: str, template_name: str, context: dict):
    # Cargar el template usando Jinja2
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    html_content = template.render(context)

    # Configuración del mensaje
    message = MIMEMultipart()
    message["From"] = settings.EMAILS_FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = subject

    # Adjuntar el contenido HTML
    message.attach(MIMEText(html_content, "html"))

    
    # Conexión al servidor SMTP usando SSL
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.starttls()  # Inicia la conexión TLS
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.EMAILS_FROM_EMAIL, to_email, message.as_string())
        print("Email sent successfully")

def send_signup_email(to_email: str, role_name: str, signup_hash: str):
    subject = "Complete Your Registration"
    signup_link = f"http://localhost:4200/signup/{signup_hash}"
    context = {
        "role_name": role_name,
        "signup_link": signup_link
    }
    send_email(to_email, subject, 'signup_template.html', context)

def send_reset_password_email(to_email: str, reset_hash: str):
    subject = "Reset Your Password"
    reset_link = f"http://localhost:4200/reset-password/{reset_hash}"
    context = {
        "reset_link": reset_link
    }
    send_email(to_email, subject, 'reset_password_template.html', context)

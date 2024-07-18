import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from core.config import settings

def send_email(to_email: str, subject: str, template_name: str, context: dict):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    html_content = template.render(context)

    message = MIMEMultipart()
    message["From"] = settings.EMAILS_FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.EMAILS_FROM_EMAIL, to_email, message.as_string())

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import settings

SMTP_CONFIG={
    "server": settings.smtp_host ,
    "port": settings.smtp_port,
    "username": settings.smtp_user,
    "password": settings.smtp_password
}

def send_message(sender_name: str, recip_email: str, message_text: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_CONFIG['username']
        msg['To'] = recip_email
        msg['Subject'] = "Message"
        
        body = f"""
        <h2>Привет! Это сообщение от {sender_name}</h2>
        <p>ваш код: {message_text}</p>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        with smtplib.SMTP(SMTP_CONFIG['server'], SMTP_CONFIG['port']) as server:
            server.starttls()
            server.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
            server.send_message(msg)
            
        return {"success": True, "error": None}

    except Exception as e:
        return {"success": False, "error": f"{e}"}
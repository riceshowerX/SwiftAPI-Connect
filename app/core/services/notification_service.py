# notification_service.py
import smtplib
from email.mime.text import MIMEText

from app.core.config import settings

class NotificationService:
    def __init__(self):
        # 从配置文件中读取 SMTP 服务器信息
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.sender_email = settings.SENDER_EMAIL
        self.sender_password = settings.SENDER_PASSWORD

    def send_email(self, receiver_email, subject, message):
        # 发送邮件通知
        try:
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = receiver_email

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, receiver_email, msg.as_string())

            logging.info(f"Successfully sent email to {receiver_email}")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
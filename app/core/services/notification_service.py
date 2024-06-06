# notification_service.py
# 此文件定义与消息通知相关的服务
import smtplib
from email.mime.text import MIMEText

class NotificationService:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        # 初始化 SMTP 服务器信息
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, receiver_email, subject, message):
        # 发送邮件通知
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = receiver_email

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, receiver_email, msg.as_string())
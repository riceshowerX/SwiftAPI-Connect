# notification_service.py
import smtplib
from email.mime.text import MIMEText
import logging
import os
from email.mime.multipart import MIMEMultipart

class NotificationService:
    def __init__(self):
        # 从环境变量中读取 SMTP 服务器信息
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')

    def send_email(self, receiver_email, subject, message, is_html=False):
        # 发送邮件通知
        try:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg.attach(MIMEText(message, 'html' if is_html else 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, receiver_email, msg.as_string())

            logging.info(f"Successfully sent email to {receiver_email}")
        except smtplib.SMTPAuthenticationError:
            logging.error("SMTP authentication error. Check the email and password.")
        except smtplib.SMTPConnectError:
            logging.error("SMTP connection error. Check the SMTP server and port.")
        except smtplib.SMTPRecipientsRefused:
            logging.error(f"Recipient {receiver_email} refused by the server.")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")

# 在模块初始化时设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

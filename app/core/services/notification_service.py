import smtplib
import logging
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import Optional

from app.core.config import settings
from smtplib import (
    SMTPException,
    SMTPAuthenticationError,
    SMTPConnectError,
    SMTPSenderRefused
)

class NotificationService:
    def __init__(self):
        """初始化邮件服务配置"""
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.sender_email = settings.SENDER_EMAIL
        self.sender_password = settings.SENDER_PASSWORD
        self.timeout = 10  # 默认超时时间（秒）

        # 验证必要配置
        if not all([self.smtp_server, self.smtp_port, self.sender_email, self.sender_password]):
            raise ValueError("SMTP配置不完整，请检查环境变量设置")

    def send_email(
        self,
        receiver_email: str,
        subject: str,
        message: str,
        is_html: bool = False,
        from_name: Optional[str] = None
    ) -> bool:
        """
        发送邮件通知
        
        Args:
            receiver_email: 收件人邮箱
            subject: 邮件主题
            message: 邮件内容
            is_html: 是否为HTML格式
            from_name: 发件人显示名称
            
        Returns:
            bool: 发送是否成功
        """
        try:
            # 验证邮箱格式
            if not self._validate_email(receiver_email):
                raise ValueError("无效的收件人邮箱格式")

            # 创建邮件
            content_type = 'html' if is_html else 'plain'
            msg = MIMEText(message, content_type, 'utf-8')
            msg['Subject'] = subject
            msg['From'] = formataddr((from_name, self.sender_email)) if from_name else self.sender_email
            msg['To'] = receiver_email

            # 建立安全连接
            with self._get_smtp_connection() as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(
                    self.sender_email,
                    receiver_email,
                    msg.as_string()
                )

            logging.info(f"邮件成功发送至 {receiver_email}")
            return True

        except SMTPAuthenticationError:
            logging.error("SMTP认证失败：用户名或密码错误")
            return False
        except SMTPConnectError:
            logging.error(f"无法连接到SMTP服务器 {self.smtp_server}:{self.smtp_port}")
            return False
        except SMTPSenderRefused:
            logging.error(f"发件人地址被拒绝：{self.sender_email}")
            return False
        except SMTPException as e:
            logging.error(f"SMTP错误：{str(e)}")
            return False
        except Exception as e:
            logging.error(f"邮件发送失败：{str(e)}")
            return False

    def _get_smtp_connection(self) -> smtplib.SMTP:
        """获取安全的SMTP连接"""
        try:
            if self.smtp_port == 465:
                # 使用SSL加密连接
                server = smtplib.SMTP_SSL(
                    self.smtp_server,
                    self.smtp_port,
                    timeout=self.timeout
                )
            else:
                # 使用STARTTLS加密
                server = smtplib.SMTP(
                    self.smtp_server,
                    self.smtp_port,
                    timeout=self.timeout
                )
                server.starttls()

            server.ehlo()
            return server

        except Exception as e:
            logging.error(f"创建SMTP连接失败：{str(e)}")
            raise

    @staticmethod
    def _validate_email(email: str) -> bool:
        """验证邮箱格式"""
        import re
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, email))
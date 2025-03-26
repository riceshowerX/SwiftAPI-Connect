from pydantic import BaseSettings, Field, validator
from typing import List, Optional
from pydantic.networks import HttpUrl
from pydantic.types import SecretStr

class Settings(BaseSettings):
    # 服务器配置
    SERVER_HOST: str = Field(
        default="127.0.0.1",
        description="服务器监听地址"
    )
    SERVER_PORT: int = Field(
        default=8015,
        description="服务器监听端口",
        gt=0, lt=65536
    )
    CORS_ORIGINS: List[HttpUrl] = Field(
        default=["http://localhost:8501"],
        description="允许的CORS源（逗号分隔的URL列表）"
    )
    
    # 安全配置
    API_KEY: SecretStr = Field(
        default=...,
        description="API认证密钥（建议通过环境变量设置）"
    )

    # 监控配置
    MONITORING_INTERVAL: int = Field(
        default=5,
        description="系统监控间隔（秒）",
        gt=0
    )
    CPU_THRESHOLD: int = Field(
        default=80,
        description="CPU使用率告警阈值（%）",
        ge=0, le=100
    )
    MEMORY_THRESHOLD: int = Field(
        default=80,
        description="内存使用率告警阈值（%）",
        ge=0, le=100
    )

    # 邮件服务配置
    SMTP_SERVER: Optional[str] = Field(
        default=None,
        description="SMTP服务器地址"
    )
    SMTP_PORT: int = Field(
        default=587,
        description="SMTP服务器端口",
        gt=0, lt=65536
    )
    SENDER_EMAIL: Optional[str] = Field(
        default=None,
        description="发件人邮箱"
    )
    SENDER_PASSWORD: Optional[SecretStr] = Field(
        default=None,
        description="发件人邮箱密码"
    )

    class Config:
        case_sensitive = True
        env_prefix = ""
        validate_assignment = True

    # 验证器
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v: str) -> List[str]:
        """解析CORS_ORIGINS环境变量"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v or []
    
    @validator("API_KEY")
    def validate_api_key(cls, v: SecretStr) -> SecretStr:
        """验证API密钥是否设置"""
        if not v.get_secret_value():
            raise ValueError("API_KEY未设置")
        return v

    @validator("SMTP_PORT", "SERVER_PORT")
    def validate_port_range(cls, v: int) -> int:
        """验证端口范围有效性"""
        if not (1 <= v <= 65535):
            raise ValueError("端口号必须在1-65535之间")
        return v

settings = Settings()
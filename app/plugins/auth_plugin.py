"""
用户认证插件模块
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.plugins.base_plugin import BasePlugin
from app.encryption import verify_password

# 硬编码的用户名和密码,实际应用中应从数据库中获取
USERS = {
    "admin": "123456"
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class AuthPlugin(BasePlugin):
    """
    用户认证插件
    """
    def setup_routes(self):
        self.router.add_api_route("/auth/token", self.get_token, methods=["POST"])
        self.router.add_api_route("/protected", self.protected_endpoint, methods=["GET"])

    async def get_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = USERS.get(form_data.username)
        if not user or not verify_password(form_data.password, user):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # 在这里可以生成和返回实际的令牌
        return {"access_token": form_data.username, "token_type": "bearer"}

    async def protected_endpoint(self, token: str = Depends(oauth2_scheme)):
        return {"message": f"Hello, {token}!"}

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from core.config import settings
from utils.token import decode_access_token

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, protected_paths: list):
        super().__init__(app)
        self.protected_paths = protected_paths
        self.security = HTTPBearer()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        for path in self.protected_paths:
            if request.url.path.startswith(path):
                credentials: HTTPAuthorizationCredentials = await self.security(request)
                if credentials:
                    token = credentials.credentials
                    try:
                        payload = decode_access_token(token)
                        if not payload:
                            raise HTTPException(status_code=403, detail="Invalid token or expired token")
                    except JWTError:
                        raise HTTPException(status_code=403, detail="Invalid token or expired token")
                else:
                    raise HTTPException(status_code=403, detail="Not authenticated")
                break
        response = await call_next(request)
        return response

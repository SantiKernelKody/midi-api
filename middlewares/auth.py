from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import HTTPException
from utils.jwt_helper import decode_access_token

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, protected_paths):
        super().__init__(app)
        self.protected_paths = protected_paths

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in self.protected_paths):
            auth_header = request.headers.get("Authorization")
            if auth_header is None or not auth_header.startswith("Bearer "):
                return Response(
                    content='{"detail": "Authorization header missing or invalid"}',
                    status_code=401,
                    media_type="application/json"
                )
            token = auth_header.split(" ")[1]
            try:
                token_data = decode_access_token(token)
                print(f"Token data in middleware: {token_data}")
                request.state.user = token_data  # Attach token data to request state
            except HTTPException as e:
                return Response(
                    content=f'{{"detail": "{e.detail}"}}',
                    status_code=e.status_code,
                    media_type="application/json"
                )
        return await call_next(request)

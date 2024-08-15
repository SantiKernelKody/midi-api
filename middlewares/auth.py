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

        # Permitir que las solicitudes OPTIONS pasen sin autenticación
        if request.method == "OPTIONS":
            response = Response(status_code=204)
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            return response

        # Si la solicitud no es OPTIONS, verificar la autenticación
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
                request.state.user = token_data  # Attach token data to request state
            except HTTPException as e:
                return Response(
                    content=f'{{"detail": "{e.detail}"}}',
                    status_code=e.status_code,
                    media_type="application/json"
                )

        # Continuar con la solicitud si todo está bien
        response = await call_next(request)
        return response

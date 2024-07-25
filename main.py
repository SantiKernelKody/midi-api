from fastapi import FastAPI
from api.v1.endpoints import games, auth
from db.session import engine
from db.base import Base
from middlewares.auth import AuthMiddleware

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Montar el middleware y especificar las rutas protegidas
#protected_paths = ["/api/v1/dashboard"]
#app.add_middleware(AuthMiddleware, protected_paths=protected_paths)

# Montar las rutas
app.include_router(games.router, prefix="/api/v1/games", tags=["games"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
#app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])
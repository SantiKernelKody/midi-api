from fastapi import FastAPI
import uvicorn
from api.v1.endpoints import games, auth, general
from db.session import engine, Base
from middlewares.auth import AuthMiddleware

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Montar el middleware y especificar las rutas protegidas
protected_paths = ["/api/v1/dashboard/general"]
app.add_middleware(AuthMiddleware, protected_paths=protected_paths)

# Montar las rutas
app.include_router(games.router, prefix="/api/v1/games", tags=["games"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(general.router, prefix="/api/v1/dashboard/general", tags=["dashboard"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)

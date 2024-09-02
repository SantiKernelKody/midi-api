from fastapi import FastAPI
import uvicorn
from api.v1.endpoints import games, auth, general, performance, user
from db.session import engine, Base
from middlewares.auth import AuthMiddleware
from starlette.middleware.cors import CORSMiddleware
from api.v1.endpoints import management
from api.v1.endpoints import game_skill

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes. Para mayor seguridad, especifica los dominios permitidos.
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)
# Montar el middleware y especificar las rutas protegidas
protected_paths = ["/api/v1/dashboard/general","/api/v1/dashboard/performance","/api/v1/dashboard/management", "/api/v1/dashboard/user",
                    "/api/v1/dashboard/skills"]
app.add_middleware(AuthMiddleware, protected_paths=protected_paths)

# Montar las rutas
app.include_router(games.router, prefix="/api/v1/games", tags=["games"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(general.router, prefix="/api/v1/dashboard/general", tags=["General"])
app.include_router(performance.router, prefix="/api/v1/dashboard/performance", tags=["Performance"])
app.include_router(management.router, prefix="/api/v1/dashboard/management", tags=["Management"])
app.include_router(user.router, prefix="/api/v1/dashboard/user", tags=["User"])
app.include_router(game_skill.router, prefix="/api/v1/dashboard/skills", tags=["Skills"])
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)

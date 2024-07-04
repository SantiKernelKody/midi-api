# app/main.py
from fastapi import FastAPI
from app.api.v1.endpoints import auth, player, game, dashboard
from app.db.session import SessionLocal

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(player.router, prefix="/api/v1/players", tags=["players"])
app.include_router(game.router, prefix="/api/v1/games", tags=["games"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])

@app.on_event("startup")
def startup():
    # Code to run on startup
    pass

@app.on_event("shutdown")
def shutdown():
    # Code to run on shutdown
    pass

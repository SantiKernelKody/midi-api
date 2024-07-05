from fastapi import FastAPI
from api.v1.endpoints import games
from db.session import engine
from db.base import Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MIDI API",
    description="API para recibir y procesar datos de juegos educativos",
    version="1.0.0"
)

# Include the router for the games endpoint
app.include_router(games.router, prefix="/api/v1/games", tags=["games"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the MIDI API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

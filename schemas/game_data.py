from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GameDataBase(BaseModel):
    nombre_juego: str
    tipo: str
    avatar_id: Optional[int] = None
    nombre_jugador: Optional[str] = None
    id_registro: Optional[int] = None
    fecha_inicio_saludo: Optional[datetime] = None
    fecha_inicio_nombre: Optional[datetime] = None
    fecha_fin_nombre: Optional[datetime] = None
    fecha_inicio_creditos: Optional[datetime] = None
    fecha_fin_creditos: Optional[datetime] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    tiempo_juego: Optional[int] = None
    estado: Optional[str] = None
    correctas: Optional[int] = None
    incorrectas: Optional[int] = None
    nombre_capitulo: Optional[str] = None
    descripcion_capitulo: Optional[str] = None
    nombre_historia: Optional[str] = None
    descripcion_historia: Optional[str] = None
    nombre_nivel: Optional[str] = None
    descripcion_nivel: Optional[str] = None
    duracion: Optional[int] = None

class GameDataCreate(GameDataBase):
    pass

class GameDataUpdate(GameDataBase):
    pass

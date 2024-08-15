from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class GameDataCreate(BaseModel):
    tipo: str
    avatar: Optional[str] = None
    nombre_juego: str
    descripcion_juego: Optional[str] = None
    nombre_capitulo: Optional[str] = None
    descripcion_capitulo: Optional[str] = None
    nombre_nivel: Optional[str] = None
    descripcion_nivel: Optional[str] = None
    correctas: Optional[int] = None
    incorrectas: Optional[int] = None
    tiempo_juego: Optional[int] = None
    duracion: Optional[int] = None
    nombre_historia: Optional[str] = None
    descripcion_historia: Optional[str] = None
    estado: Optional[str] = None
    id_registro: str
    fecha_inicio_saludo: Optional[datetime] = None
    fecha_inicio_nombre: Optional[datetime] = None
    fecha_fin_nombre: Optional[datetime] = None
    fecha_inicio_creditos: Optional[datetime] = None
    fecha_fin_creditos: Optional[datetime] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None

    @validator('fecha_inicio_saludo', 'fecha_inicio_nombre', 'fecha_fin_nombre', 
               'fecha_inicio_creditos', 'fecha_fin_creditos', 'fecha_inicio', 'fecha_fin', pre=True, always=True)
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v

    class Config:
        orm_mode = True

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from crud import game_data as crud_game_data
from schemas.game_data import GameDataCreate
from db.session import get_db
from models.educational_entity import EducationalEntity
from models.player import Player

router = APIRouter()

@router.post("/data", response_model=dict)
async def receive_game_data(request: Request, game_data: GameDataCreate, db: Session = Depends(get_db)):
    # Parse JSON data
    data = await request.json()

    # Retrieve headers (if any)
    version_header = request.headers.get('version')
    version_header = float(version_header) if version_header else None

    # Game processing
    game = crud_game_data.create_or_get_game(db, game_data.nombre_juego)
    
    # Desglosar el id_registro en school_code, stage_code y player_full_name
    if game_data.id_registro:
        registro_data = game_data.id_registro.split("-", 3)
        if len(registro_data) >= 3:
            school_code, stage_code, player_full_name = registro_data
        else:
            raise HTTPException(status_code=400, detail="Invalid id_registro format.")
    else:
        raise HTTPException(status_code=400, detail="id_registro is required.")

    # Obtener school y stage
    stage = crud_game_data.create_or_get_stage(db, stage_code)
    school = db.query(EducationalEntity).filter(EducationalEntity.code == school_code).first()

    if not school:
        school = db.query(EducationalEntity).filter(EducationalEntity.code == "ES000").first()

    # Convertir estado de español a inglés
    estado = None
    if game_data.estado:
        estado = game_data.estado.lower()
        if estado == "completado":
            estado = "completed"
        elif estado == "abandonado":
            estado = "abandoned"
        else:
            raise HTTPException(status_code=400, detail="Invalid estado value.")

    # Procesamiento de datos según el tipo
    if game_data.tipo == "jugador":
        # Procesamiento para jugador
        avatar = crud_game_data.create_or_get_avatar(db, game_data.avatar)
        player = crud_game_data.create_or_get_player(db, player_full_name, school.id)
        room = crud_game_data.create_room(db, avatar.id, player.id)  # Se omite stage_id
        
        return {"detail": "Player data saved successfully"}
    
    elif game_data.tipo == "juego":
        # Procesamiento para juego
        player = crud_game_data.create_or_get_player(db, player_full_name, school.id)
        chapter = crud_game_data.create_or_get_chapter(db, game_data.nombre_capitulo, game_data.descripcion_capitulo, game.id)
        level = crud_game_data.create_or_get_level(db, game_data.nombre_nivel, game_data.descripcion_nivel, chapter.id)
        
        player_level = crud_game_data.create_player_level(
            db=db,
            player_id=player.id,
            level_id=level.id,
            stage_id=stage.id,  # Usando el stage_id desglosado
            score=game_data.correctas,  # Assuming score is correctas
            incorrect=game_data.incorrectas,
            correct=game_data.correctas,
            attempts=1,  # Assuming attempts is 1
            total_time=game_data.tiempo_juego,  # Usando tiempo_juego como total_time
            times_out_focus=game_data.duracion,  # Assuming times_out_focus is duracion
            state=estado  # Usando el estado convertido
        )
        
        return {"detail": "Game data saved successfully"}
    
    elif game_data.tipo == "historia":
        # Procesamiento para historia
        player = crud_game_data.create_or_get_player(db, player_full_name, school.id)
        chapter = crud_game_data.create_or_get_chapter(db, game_data.nombre_capitulo, game_data.descripcion_capitulo, game.id)
        story = crud_game_data.create_or_get_story(db, game_data.nombre_historia, game_data.descripcion_historia, chapter.id)
        
        player_story = crud_game_data.create_player_story(
            db=db,
            player_id=player.id,
            story_id=story.id,
            stage_id=stage.id,  # Usando el stage_id desglosado
            time_watched=game_data.tiempo_juego,  # Usando tiempo_juego como time_watched
            total_time_out=game_data.duracion,  # Usando duracion como total_time_out
            pauses=0,  # Assuming pauses is 0
            times_out_focus=game_data.duracion,  # Assuming times_out_focus is duracion
            state=estado  # Usando el estado convertido
        )
        
        return {"detail": "Story data saved successfully"}
    
    return {"detail": "Invalid data type"}



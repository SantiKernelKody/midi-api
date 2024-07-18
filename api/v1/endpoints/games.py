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
    data = await request.json()
    
    # Retrieve headers
    version_header = request.headers.get('version')
    version_header = float(version_header) if version_header else None

    # Game processing
    game = crud_game_data.create_or_get_game(db, game_data.nombre_juego)
    game_version = float(game.version) if game.version else None
    
    if version_header and game_version and version_header < game_version:
        raise HTTPException(status_code=400, detail="Version outdated")
    
    # Player processing
    if game_data.tipo == "jugador":
        player_data = game_data.nombre_jugador.split("-", 3)
        if len(player_data) >= 3:
            school_code, stage_code, player_full_name  = player_data
        else:
            school_code = "ES000"
            stage_code = "R0"
            player_full_name  = game_data.nombre_jugador
        
        # Fetch school and stage
        stage = crud_game_data.create_or_get_stage(db, stage_code)
        school = db.query(EducationalEntity).filter(EducationalEntity.code == school_code).first()

        if not school:
            school = db.query(EducationalEntity).filter(EducationalEntity.code == "ES000").first()
        
        # Room processing
        avatar = crud_game_data.create_or_get_avatar(db, game_data.avatar)
        player = crud_game_data.create_or_get_player(db, player_full_name, school.id)
        room = crud_game_data.create_room(db, stage.id, avatar.id, player.id)
        
        return {"detail": "Player data saved successfully"}
    
    elif game_data.tipo == "juego":
        # Juego data processing
        player = db.query(Player).filter(Player.id == game_data.id_registro).first()
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        
        chapter = crud_game_data.create_or_get_chapter(db, game_data.nombre_capitulo, game_data.descripcion_capitulo, game.id)
        level = crud_game_data.create_or_get_level(db, game_data.nombre_nivel, game_data.descripcion_nivel, chapter.id)
        
        player_level = crud_game_data.create_player_level(
            db=db,
            player_id=player.id,
            level_id=level.id,
            score=game_data.correctas, # Assuming score is correctas
            incorrect=game_data.incorrectas,
            correct=game_data.correctas,
            attempts=1, # Assuming attempts is 1
            total_time=game_data.tiempo_juego,
            times_out_focus=game_data.duracion # Assuming times_out_focus is duracion
        )
        
        return {"detail": "Game data saved successfully"}
    
    elif game_data.tipo == "historia":
        # Historia data processing
        player = db.query(Player).filter(Player.id == game_data.id_registro).first()
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        
        chapter = crud_game_data.create_or_get_chapter(db, game_data.nombre_capitulo, game_data.descripcion_capitulo, game.id)
        story = crud_game_data.create_or_get_story(db, game_data.nombre_historia, game_data.descripcion_historia, chapter.id)
        
        player_story = crud_game_data.create_player_story(
            db=db,
            player_id=player.id,
            story_id=story.id,
            time_watched=game_data.tiempo_juego,
            total_time_out=game_data.duracion, # Assuming total_time_out is duracion
            pauses=0, # Assuming pauses is 0
            times_out_focus=game_data.duracion # Assuming times_out_focus is duracion
        )
        
        return {"detail": "Story data saved successfully"}
    
    return {"detail": "Invalid data type"}

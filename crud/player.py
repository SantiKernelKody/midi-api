from sqlalchemy.orm import Session
from schemas.player import PlayerCreate
from models.player import Player
from models.course_player import CoursePlayer

def create_player(db: Session, player: PlayerCreate):
    db_player = Player(
        full_name=player.full_name,
        school_id=player.school_id,
        age=player.age
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    # Crear asociación en la tabla course_player
    db_course_player = CoursePlayer(
        course_id=player.course_id,
        player_id=db_player.id
    )
    db.add(db_course_player)
    db.commit()
    db.refresh(db_course_player)

    return db_player

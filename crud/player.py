from sqlalchemy.orm import Session
from models.player import Player
from models.player_level import PlayerLevel
from schemas.player_level import PlayerLevelCreate
from models.player_story import PlayerStory
from schemas.player_story import PlayerStoryCreate

def find_player_by_name(db: Session, name: str) -> Player | None:
    player = db.query(Player).filter(Player.name == name).first()
    if not player:
        return None
    return player
def create_player_level(db: Session, player_level: PlayerLevelCreate):
    db_player_level = PlayerLevel(**player_level.dict())
    db.add(db_player_level)
    db.commit()
    db.refresh(db_player_level)
    return db_player_level

def create_player_story(db: Session, player_story: PlayerStoryCreate):
    db_player_story = PlayerStory(**player_story.dict())
    db.add(db_player_story)
    db.commit()
    db.refresh(db_player_story)
    return db_player_story
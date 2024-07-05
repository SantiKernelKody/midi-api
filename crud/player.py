from sqlalchemy.orm import Session
from models.player import Player

def find_player_by_name(db: Session, name: str):
    player = db.query(Player).filter(Player.name == name).first()
    if not player:
        return None
    return player.id
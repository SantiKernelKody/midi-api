from sqlalchemy.orm import Session
from models import Game, Player, Room, Chapter, Level, PlayerLevel, PlayerStory, EducationalEntity, Stage

def get_game_by_name(db: Session, name: str):
    return db.query(Game).filter(Game.name == name).first()

def create_game(db: Session, name: str, description: str = 'Agregar definicion'):
    db_game = Game(name=name, description=description)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def create_or_get_game(db: Session, name: str, description: str = 'Agregar definicion'):
    game = get_game_by_name(db, name)
    if not game:
        game = create_game(db, name, description)
    return game

def get_player_by_name(db: Session, name: str, school_id: int):
    return db.query(Player).filter(Player.name == name, Player.school_id == school_id).first()

def create_player(db: Session, name: str, avatar_id: int, school_id: int):
    db_player = Player(name=name, avatar_id=avatar_id, school_id=school_id)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def create_or_get_player(db: Session, name: str, avatar_id: int, school_id: int):
    player = get_player_by_name(db, name, school_id)
    if not player:
        player = create_player(db, name, avatar_id, school_id)
    return player

def create_player_level(db: Session, player_id: int, level_id: int, score: float, incorrect: int, correct: int, attempts: int, total_time: int, times_out_focus: int):
    db_player_level = PlayerLevel(player_id=player_id, level_id=level_id, score=score, incorrect=incorrect, correct=correct, attempts=attempts, total_time=total_time, times_out_focus=times_out_focus)
    db.add(db_player_level)
    db.commit()
    db.refresh(db_player_level)
    return db_player_level

def create_player_story(db: Session, player_id: int, story_id: int, time_watched: int, total_time_out: int, pauses: int, times_out_focus: int):
    db_player_story = PlayerStory(player_id=player_id, story_id=story_id, time_watched=time_watched, total_time_out=total_time_out, pauses=pauses, times_out_focus=times_out_focus)
    db.add(db_player_story)
    db.commit()
    db.refresh(db_player_story)
    return db_player_story

def get_room_by_details(db: Session, stage_id: int, school_id: int, game_id: int):
    return db.query(Room).filter(Room.stage_id == stage_id, Room.school_id == school_id, Room.game_id == game_id).first()

def create_room(db: Session, name: str, description: str, stage_id: int, school_id: int, game_id: int):
    db_room = Room(name=name, description=description, stage_id=stage_id, school_id=school_id, game_id=game_id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def create_or_get_room(db: Session, name: str, description: str, stage_id: int, school_id: int, game_id: int):
    room = get_room_by_details(db, stage_id, school_id, game_id)
    if not room:
        room = create_room(db, name, description, stage_id, school_id, game_id)
    return room

def get_chapter_by_name(db: Session, name: str, game_id: int):
    return db.query(Chapter).filter(Chapter.name == name, Chapter.game_id == game_id).first()

def create_chapter(db: Session, name: str, description: str, game_id: int):
    db_chapter = Chapter(name=name, description=description, game_id=game_id)
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter

def create_or_get_chapter(db: Session, name: str, description: str, game_id: int):
    chapter = get_chapter_by_name(db, name, game_id)
    if not chapter:
        chapter = create_chapter(db, name, description, game_id)
    return chapter

def get_level_by_name(db: Session, name: str, chapter_id: int):
    return db.query(Level).filter(Level.name == name, Level.chapter_id == chapter_id).first()

def create_level(db: Session, name: str, description: str, chapter_id: int):
    db_level = Level(name=name, description=description, chapter_id=chapter_id)
    db.add(db_level)
    db.commit()
    db.refresh(db_level)
    return db_level

def create_or_get_level(db: Session, name: str, description: str, chapter_id: int):
    level = get_level_by_name(db, name, chapter_id)
    if not level:
        level = create_level(db, name, description, chapter_id)
    return level

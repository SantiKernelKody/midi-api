from sqlalchemy.orm import Session
from models.game import Game
from models.chapter import Chapter
from models.level import Level
from models.room import Room
from models.stage import Stage
from models.avatar import Avatar
from models.player import Player
from models.player_level import PlayerLevel
from models.player_story import PlayerStory
from models.story import Story

def create_or_get_game(db: Session, name: str):
    game = db.query(Game).filter(Game.name == name).first()
    if not game:
        game = Game(name=name, description="Agregar definición")
        db.add(game)
        db.commit()
        db.refresh(game)
    return game

def create_or_get_stage(db: Session, code: str, name: str = "No definida", description: str = "No definida"):
    stage = db.query(Stage).filter(Stage.code == code).first()
    if not stage:
        stage = Stage(code=code, name=name, description=description)
        db.add(stage)
        db.commit()
        db.refresh(stage)
    return stage

def create_or_get_avatar(db: Session, name: str, description: str = "No definida"):
    avatar = db.query(Avatar).filter(Avatar.name == name).first()
    if not avatar:
        avatar = Avatar(name=name, description=description)
        db.add(avatar)
        db.commit()
        db.refresh(avatar)
    return avatar

def create_or_get_player(db: Session, full_name: str, school_id: int):
    player = db.query(Player).filter(Player.full_name == full_name, Player.school_id == school_id).first()
    if not player:
        player = Player(full_name=full_name, school_id=school_id, user_name=full_name, password="default_password")
        db.add(player)
        db.commit()
        db.refresh(player)
    return player

def create_or_get_chapter(db: Session, name: str, description: str, game_id: int):
    chapter = db.query(Chapter).filter(Chapter.name == name, Chapter.game_id == game_id).first()
    if not chapter:
        chapter = Chapter(name=name, description=description, game_id=game_id)
        db.add(chapter)
        db.commit()
        db.refresh(chapter)
    return chapter

def create_or_get_level(db: Session, name: str, description: str, chapter_id: int):
    level = db.query(Level).filter(Level.name == name, Level.chapter_id == chapter_id).first()
    if not level:
        level = Level(name=name, description=description, chapter_id=chapter_id)
        db.add(level)
        db.commit()
        db.refresh(level)
    return level

def create_or_get_story(db: Session, name: str, description: str, chapter_id: int):
    story = db.query(Story).filter(Story.name == name, Story.chapter_id == chapter_id).first()
    if not story:
        story = Story(name=name, description=description, chapter_id=chapter_id)
        db.add(story)
        db.commit()
        db.refresh(story)
    return story

def create_room(db: Session, avatar_id: int, player_id: int):
    room = Room(id_avatar=avatar_id, player_id=player_id)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def create_player_level(db: Session, player_id: int, level_id: int, stage_id: int, score: float, incorrect: int, correct: int, attempts: int, total_time: int, times_out_focus: int):
    player_level = PlayerLevel(
        player_id=player_id,
        level_id=level_id,
        stage_id=stage_id,
        score=score,
        incorrect=incorrect,
        correct=correct,
        attempts=attempts,
        total_time=total_time,
        times_out_focus=times_out_focus
    )
    db.add(player_level)
    db.commit()
    db.refresh(player_level)
    return player_level

def create_player_story(db: Session, player_id: int, story_id: int, stage_id: int, time_watched: int, total_time_out: int, pauses: int, times_out_focus: int):
    player_story = PlayerStory(
        player_id=player_id,
        story_id=story_id,
        stage_id=stage_id,
        time_watched=time_watched,
        total_time_out=total_time_out,
        pauses=pauses,
        times_out_focus=times_out_focus
    )
    db.add(player_story)
    db.commit()
    db.refresh(player_story)
    return player_story

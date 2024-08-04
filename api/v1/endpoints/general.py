from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from schemas import *
from models.game import Game
from models.chapter import Chapter
from models.level import Level
from models.player import Player
from models.dashboard_user import DashboardUser
from models.course import Course
from models.player_level import PlayerLevel
from models.player_story import PlayerStory
from models.story import Story
from db.session import SessionLocal
from token import get_current_user

router = APIRouter()

@router.get("/games", response_model=List[Game])
def get_game_list(db: Session = Depends(SessionLocal), current_user: DashboardUser = Depends(get_current_user)):
    return db.query(Game).all()

@router.get("/general-headers/admin")
def get_general_headers_admin(db: Session = Depends(SessionLocal), current_user: DashboardUser = Depends(get_current_user)):
    total_kids = db.query(Player).filter(Player.school_id.isnot(None)).count()
    total_games = db.query(Game).count()
    total_chapters = db.query(Chapter).count()
    total_levels = db.query(Level).count()
    return {
        "total_kids": total_kids,
        "total_games": total_games,
        "total_chapters": total_chapters,
        "total_levels": total_levels
    }

@router.get("/game-header/admin/{game_id}")
def get_game_header_admin(game_id: int, db: Session = Depends(SessionLocal), current_user: DashboardUser = Depends(get_current_user)):
    total_kids_played = db.query(PlayerLevel).join(Level).join(Chapter).filter(Chapter.game_id == game_id).count()
    total_chapters = db.query(Chapter).filter(Chapter.game_id == game_id).count()
    total_levels = db.query(Level).join(Chapter).filter(Chapter.game_id == game_id).count()
    return {
        "total_kids_played": total_kids_played,
        "total_chapters": total_chapters,
        "total_levels": total_levels
    }

@router.get("/general-headers/teacher")
def get_general_headers_teacher(db: Session = Depends(SessionLocal), current_user: DashboardUser = Depends(get_current_user)):
    courses = db.query(Course).filter(Course.reviewer_id == current_user.id).all()
    return courses

@router.get("/game-header/teacher/{game_id}")
def get_game_header_teacher(game_id: int, db: Session = Depends(SessionLocal), current_user: DashboardUser = Depends(get_current_user)):
    courses = db.query(Course).filter(Course.reviewer_id == current_user.id).all()
    course_ids = [course.id for course in courses]
    total_kids_played = db.query(PlayerLevel).join(Player).join(CoursePlayer).filter(CoursePlayer.course_id.in_(course_ids), PlayerLevel.level.has(Chapter.game_id == game_id)).count()
    courses_with_kids_played = db.query(Course).join(CoursePlayer).join(PlayerLevel).filter(Course.reviewer_id == current_user.id, PlayerLevel.level.has(Chapter.game_id == game_id)).distinct().count()
    return {
        "total_kids_played": total_kids_played,
        "courses_with_kids_played": courses_with_kids_played
    }

@router.get("/kids")
def get_kid_list(db: Session = Depends(SessionLocal), current_user: DashboardUser = Depends(get_current_user)):
    kids = db.query(Player).join(CaretakerPlayer).filter(CaretakerPlayer.representative_id == current_user.id).all()
    return kids

@router.get("/general-body/admin/{game_id}")
def get_general_body_admin(game_id: int, db: Session = Depends(SessionLocal), current_user: DashboardUser = Depends(get_current_user)):
    chapters = db.query(Chapter).filter(Chapter.game_id == game_id).all()
    chapter_ids = [chapter.id for chapter in chapters]

    chapter_grades = []
    chapter_times = []
    chapter_states = []
    story_states = []

    for chapter in chapters:
        levels = db.query(Level).filter(Level.chapter_id == chapter.id).all()
        level_ids = [level.id for level in levels]

        avg_scores = db.query(func.avg(PlayerLevel.score)).filter(PlayerLevel.level_id.in_(level_ids)).scalar()
        avg_time = db.query(func.avg(PlayerLevel.total_time)).filter(PlayerLevel.level_id.in_(level_ids)).scalar()

        completed = db.query(PlayerLevel).filter(PlayerLevel.level_id.in_(level_ids), PlayerLevel.state == "completed").count()
        abandoned = db.query(PlayerLevel).filter(PlayerLevel.level_id.in_(level_ids), PlayerLevel.state == "abandoned").count()

        chapter_grades.append(avg_scores)
        chapter_times.append(avg_time)
        chapter_states.append({"label": "Completed", "data": completed})
        chapter_states.append({"label": "Abandoned", "data": abandoned})

        stories = db.query(Story).filter(Story.chapter_id == chapter.id).all()
        for story in stories:
            completed = db.query(PlayerStory).filter(PlayerStory.story_id == story.id, PlayerStory.state == "completed").count()
            abandoned = db.query(PlayerStory).filter(PlayerStory.story_id == story.id, PlayerStory.state == "abandoned").count()
            story_states.append({"label": "Completed", "data": completed})
            story_states.append({"label": "Abandoned", "data": abandoned})

    return {
        "chapter_grades": {"labels": [chapter.name for chapter in chapters], "data": chapter_grades},
        "chapter_times": {"labels": [chapter.name for chapter in chapters], "data": chapter_times},
        "chapter_states": {"labels": [chapter.name for chapter in chapters], "data": chapter_states},
        "story_states": {"labels": [story.name for story in stories], "data": story_states},
    }

@router.get("/general-body/teacher/{game_id}")
def get_general_body_teacher(game_id: int, db: Session = Depends(SessionLocal), current_user: DashboardUser = Depends(get_current_user)):
    courses = db.query(Course).filter(Course.reviewer_id == current_user.id).all()
    course_ids = [course.id for course in courses]
    players = db.query(Player).join(CoursePlayer).filter(CoursePlayer.course_id.in_(course_ids)).all()
    player_ids = [player.id for player in players]
    
    chapters = db.query(Chapter).filter(Chapter.game_id == game_id).all()
    chapter_ids = [chapter.id for chapter in chapters]

    chapter_grades = []
    chapter_times = []
    chapter_states = []
    story_states = []

    for chapter in chapters:
        levels = db.query(Level).filter(Level.chapter_id == chapter.id).all()
        level_ids = [level.id for level in levels]

        avg_scores = db.query(func.avg(PlayerLevel.score)).filter(PlayerLevel.level_id.in_(level_ids), PlayerLevel.player_id.in_(player_ids)).scalar()
        avg_time = db.query(func.avg(PlayerLevel.total_time)).filter(PlayerLevel.level_id.in_(level_ids), PlayerLevel.player_id.in_(player_ids)).scalar()

        completed = db.query(PlayerLevel).filter(PlayerLevel.level_id.in_(level_ids), PlayerLevel.state == "completed", PlayerLevel.player_id.in_(player_ids)).count()
        abandoned = db.query(PlayerLevel).filter(PlayerLevel.level_id.in_(level_ids), PlayerLevel.state == "abandoned", PlayerLevel.player_id.in_(player_ids)).count()

        chapter_grades.append(avg_scores)
        chapter_times.append(avg_time)
        chapter_states.append({"label": "Completed", "data": completed})
        chapter_states.append({"label": "Abandoned", "data": abandoned})

        stories = db.query(Story).filter(Story.chapter_id == chapter.id).all()
        for story in stories:
            completed = db.query(PlayerStory).filter(PlayerStory.story_id == story.id, PlayerStory.state == "completed", PlayerStory.player_id.in_(player_ids)).count()
            abandoned = db.query(PlayerStory).filter(PlayerStory.story_id == story.id, PlayerStory.state == "abandoned", PlayerStory.player_id.in_(player_ids)).count()
            story_states.append({"label": "Completed", "data": completed})
            story_states.append({"label": "Abandoned", "data": abandoned})

    return {
        "chapter_grades": {"labels": [chapter.name for chapter in chapters], "data": chapter_grades},
        "chapter_times": {"labels": [chapter.name for chapter in chapters], "data": chapter_times},
        "chapter_states": {"labels": [chapter.name for chapter in chapters], "data": chapter_states},
        "story_states": {"labels": [story.name for story in stories], "data": story_states},
    }

@router.get("/general-body/parent/{game_id}/{player_id}")
def get_general_body_parent(game_id: int, player_id: int, db: Session = Depends(SessionLocal), current_user: DashboardUser = Depends(get_current_user)):
    chapters = db.query(Chapter).filter(Chapter.game_id == game_id).all()
    chapter_ids = [chapter.id for chapter in chapters]

    chapter_grades = []
    chapter_times = []
    chapter_states = []
    story_states = []

    for chapter in chapters:
        levels = db.query(Level).filter(Level.chapter_id == chapter.id).all()
        level_ids = [level.id for level in levels]

        avg_scores = db.query(func.avg(PlayerLevel.score)).filter(PlayerLevel.level_id.in_(level_ids), PlayerLevel.player_id == player_id).scalar()
        avg_time = db.query(func.avg(PlayerLevel.total_time)).filter(PlayerLevel.level_id.in_(level_ids), PlayerLevel.player_id == player_id).scalar()

        completed = db.query(PlayerLevel).filter(PlayerLevel.level_id.in_(level_ids), PlayerLevel.state == "completed", PlayerLevel.player_id == player_id).count()
        abandoned = db.query(PlayerLevel).filter(PlayerLevel.level_id.in_(level_ids), PlayerLevel.state == "abandoned", PlayerLevel.player_id == player_id).count()

        chapter_grades.append(avg_scores)
        chapter_times.append(avg_time)
        chapter_states.append({"label": "Completed", "data": completed})
        chapter_states.append({"label": "Abandoned", "data": abandoned})

        stories = db.query(Story).filter(Story.chapter_id == chapter.id).all()
        for story in stories:
            completed = db.query(PlayerStory).filter(PlayerStory.story_id == story.id, PlayerStory.state == "completed", PlayerStory.player_id == player_id).count()
            abandoned = db.query(PlayerStory).filter(PlayerStory.story_id == story.id, PlayerStory.state == "abandoned", PlayerStory.player_id == player_id).count()
            story_states.append({"label": "Completed", "data": completed})
            story_states.append({"label": "Abandoned", "data": abandoned})

    return {
        "chapter_grades": {"labels": [chapter.name for chapter in chapters], "data": chapter_grades},
        "chapter_times": {"labels": [chapter.name for chapter in chapters], "data": chapter_times},
        "chapter_states": {"labels": [chapter.name for chapter in chapters], "data": chapter_states},
        "story_states": {"labels": [story.name for story in stories], "data": story_states},
    }

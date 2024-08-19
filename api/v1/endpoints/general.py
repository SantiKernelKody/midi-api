from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.game import Game as GameModel
from schemas.game import Game as GameSchema
from utils.email import send_signup_email
from utils.jwt_helper import  get_current_user
from models.dashboard_user import DashboardUser
from models.player import Player
from models.chapter import Chapter
from models.level import Level
from models.player_level import PlayerLevel
from models.story import Story
from models.player_story import PlayerStory
from models.course import Course
from models.course_player import CoursePlayer
from models.caretaker_player import CaretakerPlayer
from db.session import get_db
from models.user_role import UserRole as UserRoleModel
router = APIRouter()

@router.get("/get_user_info")
def get_user_info(
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user)
):
    # Buscar al usuario actual usando el current_user
    user = db.query(DashboardUser).filter(DashboardUser.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Buscar el rol del usuario
    role = db.query(UserRoleModel).filter(UserRoleModel.id == user.role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return {
        "name": f"{user.name} {user.last_name}",
        "role_name": role.name
    }

@router.get("/games", response_model=List[GameSchema])
def get_games(db: Session = Depends(get_db), current_user: DashboardUser = Depends(get_current_user)):
    print(f"Current user in route: {current_user}")
    games = db.query(GameModel).all()
    return games

@router.post("/send-signup-email")
def send_signup_email_route():
    try:
        send_signup_email('tagoandres2000@hotmail.com', 'Padre de familia', 'prueba_hash')
        return {"message": "Sign-up email sent"}
    except Exception as e:
        print(f"Error sending email: {e}")
        return {"message": "Failed to send sign-up email"}, 500

@router.get("/general_headers_admin")
def get_general_headers_admin(db: Session = Depends(get_db)):
    total_players = db.query(Player).filter(Player.school_id.isnot(None)).count()
    total_games = db.query(GameModel).count()
    total_chapters = db.query(Chapter).count()
    total_levels = db.query(Level).count()
    return {
        "total_players": total_players,
        "total_games": total_games,
        "total_chapters": total_chapters,
        "total_levels": total_levels,
    }

@router.get("/game_header_admin/{game_id}", response_model=dict)
def get_game_header_admin(game_id: int, db: Session = Depends(get_db), current_user: DashboardUser = Depends(get_current_user)):
    # Obtener todos los capítulos relacionados con el juego
    chapters = db.query(Chapter).filter(Chapter.game_id == game_id).all()
    
    # Obtener los niveles relacionados con estos capítulos
    chapter_ids = [chapter.id for chapter in chapters]
    levels = db.query(Level).filter(Level.chapter_id.in_(chapter_ids)).all()
    
    # Contar los jugadores que han jugado estos niveles
    level_ids = [level.id for level in levels]
    total_players = db.query(PlayerLevel).filter(PlayerLevel.level_id.in_(level_ids)).count()
    
    return {
        "total_players": total_players,
        "total_levels": len(levels),
        "total_chapters": len(chapters)
    }

@router.get("/general_headers_teacher", response_model=dict)
def get_general_headers_teacher(db: Session = Depends(get_db), current_user: DashboardUser = Depends(get_current_user)):
    # Obtener el número de cursos que ha creado el usuario
    total_courses = db.query(Course).filter(Course.reviewer_id == current_user.id).count()
    
    # Obtener todos los cursos creados por el usuario
    courses = db.query(Course).filter(Course.reviewer_id == current_user.id).all()
    course_ids = [course.id for course in courses]
    
    # Contar el número total de niños en esos cursos
    total_players = db.query(CoursePlayer).filter(CoursePlayer.course_id.in_(course_ids)).count()
    
    return {
        "total_courses": total_courses,
        "total_players": total_players
    }
@router.get("/game_header_teacher/{game_id}", response_model=dict)
def get_game_header_teacher(game_id: int, db: Session = Depends(get_db), current_user: DashboardUser = Depends(get_current_user)):
    # Obtener cursos creados por el profesor
    courses = db.query(Course).filter(Course.reviewer_id == current_user.id).all()
    course_ids = [course.id for course in courses]

    # Obtener todos los niños en los cursos del profesor
    player_ids = db.query(CoursePlayer.player_id).filter(CoursePlayer.course_id.in_(course_ids)).all()
    player_ids = [player_id[0] for player_id in player_ids]

    # Contar el número de niños que han jugado el juego
    total_players = db.query(PlayerLevel).join(Level).join(Chapter).filter(
        PlayerLevel.player_id.in_(player_ids),
        Chapter.game_id == game_id
    ).count()

    # Contar el número de cursos donde al menos un niño ha jugado el juego
    total_courses = db.query(Course).join(CoursePlayer).join(PlayerLevel, PlayerLevel.player_id == CoursePlayer.player_id).join(Level).join(Chapter).filter(
        Course.reviewer_id == current_user.id,
        Chapter.game_id == game_id
    ).distinct().count()

    return {
        "total_players": total_players,
        "total_courses": total_courses
    }


@router.get("/kid_list")
def get_kid_list(current_user: DashboardUser = Depends(get_current_user), db: Session = Depends(get_db)):
    kids = db.query(Player).join(CaretakerPlayer).filter(CaretakerPlayer.representative_id == current_user.id).all()
    return kids

@router.get("/general_body_admin/{game_id}")
def get_general_body_admin(game_id: int, db: Session = Depends(get_db)):
    levels = db.query(Level).join(Chapter).filter(Chapter.game_id == game_id).all()
    level_grades = {"labels": [], "data": []}
    level_times = {"labels": [], "data": []}
    level_states = {"labels": [], "data": []}
    story_states = {"labels": [], "data": []}

    for level in levels:
        level_data = db.query(PlayerLevel).filter(PlayerLevel.level_id == level.id).all()
        scores = [data.score for data in level_data]
        times = [data.total_time for data in level_data]
        states = [data.state for data in level_data]
        completed = states.count('completed')
        abandoned = states.count('abandoned')
        level_grades["labels"].append(level.name)
        level_grades["data"].append(sum(scores) / len(scores) if scores else 0)
        level_times["labels"].append(level.name)
        level_times["data"].append(sum(times) / len(times) if times else 0)
        level_states["labels"].append(level.name)
        level_states["data"].append({
            "label": "Completados",
            "data": completed
        })
        level_states["data"].append({
            "label": "Abandonados",
            "data": abandoned
        })

    stories = db.query(Story).join(Chapter).filter(Chapter.game_id == game_id).all()
    for story in stories:
        story_data = db.query(PlayerStory).filter(PlayerStory.story_id == story.id).all()
        story_completed = 0
        story_abandoned = 0
        for data in story_data:
            if data.state == 'completed':
                story_completed += 1
            else:
                story_abandoned += 1
        story_states["labels"].append(story.name)
        story_states["data"].append({
            "label": "Completados",
            "data": story_completed
        })
        story_states["data"].append({
            "label": "Abandonados",
            "data": story_abandoned
        })

    return {
        "level_grades": level_grades,
        "level_times": level_times,
        "level_states": {
            "labels": level_states["labels"],
            "data": [
                {
                    "label": "Completados",
                    "data": [state["data"] for state in level_states["data"] if state["label"] == "Completados"]
                },
                {
                    "label": "Abandonados",
                    "data": [state["data"] for state in level_states["data"] if state["label"] == "Abandonados"]
                }
            ]
        },
        "story_states": {
            "labels": story_states["labels"],
            "data": [
                {
                    "label": "Completados",
                    "data": [state["data"] for state in story_states["data"] if state["label"] == "Completados"]
                },
                {
                    "label": "Abandonados",
                    "data": [state["data"] for state in story_states["data"] if state["label"] == "Abandonados"]
                }
            ]
        }
    }

@router.get("/general_body_teacher/{game_id}")
def get_general_body_teacher(game_id: int, current_user: DashboardUser = Depends(get_current_user), db: Session = Depends(get_db)):
    levels = db.query(Level).join(Chapter).filter(Chapter.game_id == game_id).all()
    level_grades = {"labels": [], "data": []}
    level_times = {"labels": [], "data": []}
    level_states = {"labels": [], "data": []}
    story_states = {"labels": [], "data": []}

    for level in levels:
        level_data = db.query(PlayerLevel).join(Player).join(CoursePlayer).join(Course).filter(
            PlayerLevel.level_id == level.id,
            Course.reviewer_id == current_user.id
        ).all()
        scores = [data.score for data in level_data]
        times = [data.total_time for data in level_data]
        states = [data.state for data in level_data]
        completed = states.count('completed')
        abandoned = states.count('abandoned')
        level_grades["labels"].append(level.name)
        level_grades["data"].append(sum(scores) / len(scores) if scores else 0)
        level_times["labels"].append(level.name)
        level_times["data"].append(sum(times) / len(times) if times else 0)
        level_states["labels"].append(level.name)
        level_states["data"].append({
            "label": "Completados",
            "data": completed
        })
        level_states["data"].append({
            "label": "Abandonados",
            "data": abandoned
        })

    stories = db.query(Story).join(Chapter).filter(Chapter.game_id == game_id).all()
    for story in stories:
        story_data = db.query(PlayerStory).join(Player).join(CoursePlayer).join(Course).filter(
            PlayerStory.story_id == story.id,
            Course.reviewer_id == current_user.id
        ).all()
        story_completed = 0
        story_abandoned = 0
        for data in story_data:
            if data.state == 'completed':
                story_completed += 1
            else:
                story_abandoned += 1
        story_states["labels"].append(story.name)
        story_states["data"].append({
            "label": "Completados",
            "data": story_completed
        })
        story_states["data"].append({
            "label": "Abandonados",
            "data": story_abandoned
        })

    return {
        "level_grades": level_grades,
        "level_times": level_times,
        "level_states": {
            "labels": level_states["labels"],
            "data": [
                {
                    "label": "Completados",
                    "data": [state["data"] for state in level_states["data"] if state["label"] == "Completados"]
                },
                {
                    "label": "Abandonados",
                    "data": [state["data"] for state in level_states["data"] if state["label"] == "Abandonados"]
                }
            ]
        },
        "story_states": {
            "labels": story_states["labels"],
            "data": [
                {
                    "label": "Completados",
                    "data": [state["data"] for state in story_states["data"] if state["label"] == "Completados"]
                },
                {
                    "label": "Abandonados",
                    "data": [state["data"] for state in story_states["data"] if state["label"] == "Abandonados"]
                }
            ]
        }
    }

@router.get("/general_body_parent/{game_id}/{player_id}")
def get_general_body_parent(game_id: int, player_id: int, current_user: DashboardUser = Depends(get_current_user), db: Session = Depends(get_db)):
    levels = db.query(Level).join(Chapter).filter(Chapter.game_id == game_id).all()
    level_grades = {"labels": [], "data": []}
    level_times = {"labels": [], "data": []}
    level_states = {"labels": [], "data": []}
    story_states = {"labels": [], "data": []}

    for level in levels:
        level_data = db.query(PlayerLevel).filter(
            PlayerLevel.level_id == level.id,
            PlayerLevel.player_id == player_id
        ).all()
        scores = [data.score for data in level_data]
        times = [data.total_time for data in level_data]
        states = [data.state for data in level_data]
        completed = states.count('completed')
        abandoned = states.count('abandoned')
        level_grades["labels"].append(level.name)
        level_grades["data"].append(sum(scores) / len(scores) if scores else 0)
        level_times["labels"].append(level.name)
        level_times["data"].append(sum(times) / len(times) if times else 0)
        level_states["labels"].append(level.name)
        level_states["data"].append({
            "label": "Completados",
            "data": completed
        })
        level_states["data"].append({
            "label": "Abandonados",
            "data": abandoned
        })

    stories = db.query(Story).join(Chapter).filter(Chapter.game_id == game_id).all()
    for story in stories:
        story_data = db.query(PlayerStory).filter(
            PlayerStory.story_id == story.id,
            PlayerStory.player_id == player_id
        ).all()
        story_completed = 0
        story_abandoned = 0
        for data in story_data:
            if data.state == 'completed':
                story_completed += 1
            else:
                story_abandoned += 1
        story_states["labels"].append(story.name)
        story_states["data"].append({
            "label": "Completados",
            "data": story_completed
        })
        story_states["data"].append({
            "label": "Abandonados",
            "data": story_abandoned
        })

    return {
        "level_grades": level_grades,
        "level_times": level_times,
        "level_states": {
            "labels": level_states["labels"],
            "data": [
                {
                    "label": "Completados",
                    "data": [state["data"] for state in level_states["data"] if state["label"] == "Completados"]
                },
                {
                    "label": "Abandonados",
                    "data": [state["data"] for state in level_states["data"] if state["label"] == "Abandonados"]
                }
            ]
        },
        "story_states": {
            "labels": story_states["labels"],
            "data": [
                {
                    "label": "Completados",
                    "data": [state["data"] for state in story_states["data"] if state["label"] == "Completados"]
                },
                {
                    "label": "Abandonados",
                    "data": [state["data"] for state in story_states["data"] if state["label"] == "Abandonados"]
                }
            ]
        }
    }
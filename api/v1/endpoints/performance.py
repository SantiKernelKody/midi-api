from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import date

from crud.user_role import is_admin, is_teacher
from models.caretaker_player import CaretakerPlayer
from schemas.stage import StageBase
from schemas.educational_entity import EducationalEntityBase
from models import Stage, EducationalEntity, EducationReviewer, PlayerLevel, PlayerStory, Course, DashboardUser, Chapter, Player, Level, Story, CoursePlayer
from db.session import get_db
from utils.jwt_helper import get_current_user
from schemas.educational_entity import EducationalEntity as EducationalEntitySchema

COLORS = ["#FFCE56", "#82BEFF", "#EE6B4D", "#3D5B81"]
router = APIRouter()

@router.get("/get_stages", response_model=List[StageBase])
def get_stages(db: Session = Depends(get_db)):
    stages = db.query(Stage).all()
    return stages

@router.get("/get_schools", response_model=List[EducationalEntitySchema])
def get_schools(
    current_user: DashboardUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if is_admin(current_user, db):
        # Si es admin, devolver todas las escuelas
        schools = db.query(EducationalEntity).all()
    elif is_teacher(current_user, db):
        # Si es teacher, devolver solo las escuelas con las que está asociado
        schools = db.query(EducationalEntity)\
            .join(EducationReviewer, EducationReviewer.education_id == EducationalEntity.id)\
            .filter(EducationReviewer.reviewer_id == current_user.id).all()
    else:
        raise HTTPException(status_code=403, detail="Not authorized to access schools")

    return schools

@router.get("/get_courses")
def get_courses(
    school_id: int = Query(...),
    current_user: DashboardUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # Consulta básica de cursos basada en el school_id
    courses_query = db.query(Course).filter(Course.school_id == school_id)
    
    # Si el usuario no es admin, filtrar solo los cursos creados por el profesor
    if current_user.role_id != 1:  # Verifica que no sea admin
        courses_query = courses_query.filter(Course.reviewer_id == current_user.id)

    # Obtener la lista de cursos
    courses = courses_query.all()

    # Preparar la respuesta con nombre e id de cada curso
    course_list = [{"id": course.id, "name": course.subject_name} for course in courses]

    return {
        "courses": course_list
    }

@router.get("/get_performance_school")
def get_performance_school(
    school_id: int = Query(...),
    start_date: date = Query(...),
    end_date: date = Query(...),
    stage_id: int = Query(...),
    game_id: int = Query(...),
    current_user: DashboardUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    levels = db.query(Level)\
        .join(Chapter)\
        .filter(Chapter.game_id == game_id)\
        .order_by(asc(Level.id))\
        .all()
    level_grades = {"labels": [], "data": []}
    level_times = {"labels": [], "data": []}
    level_states = {"labels": [], "data": []}
    story_states = {"labels": [], "data": []}
    story_times = {"labels": [], "data": []}
    course_list = []

    # Verificar si el stage es "Todos"
    stage = db.query(Stage).filter(Stage.id == stage_id).first()
    filter_by_stage = stage.code != "Todos" if stage else True

    for level in levels:
        level_data_query = db.query(PlayerLevel).join(Player).join(CoursePlayer).join(Course).filter(
            PlayerLevel.level_id == level.id,
            PlayerLevel.created_at.between(start_date, end_date),
            Course.school_id == school_id  # Filtrar por escuela
        )

        if filter_by_stage:  # Filtrar por stage solo si no es "Todos"
            level_data_query = level_data_query.filter(PlayerLevel.stage_id == stage_id)
        
        if current_user.role_id != 1:  # Si no es admin, filtrar por cursos del profesor
            level_data_query = level_data_query.filter(Course.reviewer_id == current_user.id)
        
        level_data = level_data_query.all()
        scores = [data.score for data in level_data]
        times = [data.total_time for data in level_data]
        states = [data.state for data in level_data]

        level_grades["labels"].append(level.name)
        level_grades["data"].append(round(sum(scores) / len(scores), 2) if scores else 0)
        level_times["labels"].append(level.name)
        level_times["data"].append(round(sum(times) / len(times), 2) if times else 0)

        completed = states.count('completed')
        abandoned = states.count('abandoned')

        level_states["labels"].append(level.name)
        level_states["data"].append({
            "label": "Completados",
            "data": completed
        })
        level_states["data"].append({
            "label": "Abandonados",
            "data": abandoned
        })

    # Procesar historias
    stories = db.query(Story).join(Chapter).filter(Chapter.game_id == game_id).all()
    for story in stories:
        story_data_query = db.query(PlayerStory).join(Player).join(CoursePlayer).join(Course).filter(
            PlayerStory.story_id == story.id,
            PlayerStory.created_at.between(start_date, end_date),
            Course.school_id == school_id  # Filtrar por escuela
        )

        if filter_by_stage:  # Filtrar por stage solo si no es "Todos"
            story_data_query = story_data_query.filter(PlayerStory.stage_id == stage_id)

        if current_user.role_id != 1:  # Si no es admin, filtrar por cursos del profesor
            story_data_query = story_data_query.filter(Course.reviewer_id == current_user.id)

        story_data = story_data_query.all()
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
        story_times["labels"].append(story.name)
        story_times["data"].append(round(sum([data.time_watched for data in story_data]) / len(story_data), 2) if story_data else 0)

    # Lista de cursos y sus promedios
    courses_query = db.query(Course).filter(Course.school_id == school_id)
    if current_user.role_id != 1:  # Si no es admin, filtrar por cursos del profesor
        courses_query = courses_query.filter(Course.reviewer_id == current_user.id)

    courses = courses_query.all()
    for course in courses:
        course_students = db.query(PlayerLevel).join(Player).join(CoursePlayer).filter(
            CoursePlayer.course_id == course.id,
            PlayerLevel.created_at.between(start_date, end_date)
        ).all()
        average_score = round(sum([data.score for data in course_students]) / len(course_students), 2) if course_students else 0
        course_list.append({"name_curso": course.subject_name, "id_curso": course.id, "promedio_curso_juego": average_score})

    return {
        "level_grades": level_grades,
        "level_times": level_times,
        "level_states": {
            "labels": level_states["labels"],
            "data": [
                {
                    "label": "Completados",
                    "data": [state["data"] for state in level_states["data"] if state["label"] == "Completados"],
                    "backgroundColor": COLORS[0]
                },
                {
                    "label": "Abandonados",
                    "data": [state["data"] for state in level_states["data"] if state["label"] == "Abandonados"],
                    "backgroundColor": COLORS[1]
                }
            ]
        },
        "story_states": {
            "labels": story_states["labels"],
            "data": [
                {
                    "label": "Completados",
                    "data": [state["data"] for state in story_states["data"] if state["label"] == "Completados"],
                    "backgroundColor": COLORS[2]
                },
                {
                    "label": "Abandonados",
                    "data": [state["data"] for state in story_states["data"] if state["label"] == "Abandonados"],
                    "backgroundColor": COLORS[3]
                }
            ]
        },
        "story_times": story_times,
        "Course_list": course_list,
    }

@router.get("/get_performance_course")
def get_performance_course(
    course_id: int = Query(...),
    start_date: date = Query(...),
    end_date: date = Query(...),
    stage_id: int = Query(...),
    game_id: int = Query(...),
    current_user: DashboardUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # Validar que el curso existe y que el profesor es el creador si no es admin
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if current_user.role_id != 1 and course.reviewer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this course")

    # Obtener niveles asociados al juego
    levels = db.query(Level)\
        .join(Chapter)\
        .filter(Chapter.game_id == game_id)\
        .order_by(asc(Level.id))\
        .all()
    level_grades = {"labels": [], "data": []}
    level_times = {"labels": [], "data": []}
    level_states = {"labels": [], "data": []}
    story_states = {"labels": [], "data": []}
    story_times = {"labels": [], "data": []}
    student_list = []

    # Verificar si el stage es "Todos"
    stage = db.query(Stage).filter(Stage.id == stage_id).first()
    filter_by_stage = stage.code != "Todos" if stage else True
    for level in levels:
        level_data_query = db.query(PlayerLevel).join(Player).join(CoursePlayer).filter(
            PlayerLevel.level_id == level.id,
            PlayerLevel.created_at.between(start_date, end_date),
            CoursePlayer.course_id == course_id
        )
        if filter_by_stage:  # Filtrar por stage solo si no es "Todos"
            level_data_query = level_data_query.filter(PlayerLevel.stage_id == stage_id)
        
        level_data = level_data_query.all()
        scores = [data.score for data in level_data]
        times = [data.total_time for data in level_data]
        states = [data.state for data in level_data]
        level_grades["labels"].append(level.name)
        level_grades["data"].append(round(sum(scores) / len(scores), 2) if scores else 0)
        level_times["labels"].append(level.name)
        level_times["data"].append(round(sum(times) / len(times), 2) if times else 0)
        completed = states.count('completed')
        abandoned = states.count('abandoned')
        level_states["labels"].append(level.name)
        level_states["data"].append({
            "label": "Completados",
            "data": completed
        })
        level_states["data"].append({
            "label": "Abandonados",
            "data": abandoned
        })

    # Procesar historias
    stories = db.query(Story).join(Chapter).filter(Chapter.game_id == game_id).all()
    for story in stories:
        story_data_query = db.query(PlayerStory).join(Player).join(CoursePlayer).filter(
            PlayerStory.story_id == story.id,
            PlayerStory.created_at.between(start_date, end_date),
            CoursePlayer.course_id == course_id
        )
        if filter_by_stage:  # Filtrar por stage solo si no es "Todos"
            story_data_query = story_data_query.filter(PlayerStory.stage_id == stage_id)
        
        story_data = story_data_query.all()
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
        story_times["labels"].append(story.name)
        story_times["data"].append(round(sum([data.time_watched for data in story_data]) / len(story_data), 2) if story_data else 0)

    # Lista de estudiantes y sus promedios
    students = db.query(Player).join(CoursePlayer).filter(CoursePlayer.course_id == course_id).all()
    for student in students:
        student_levels = db.query(PlayerLevel).filter(
            PlayerLevel.player_id == student.id,
            PlayerLevel.created_at.between(start_date, end_date),
            PlayerLevel.level_id.in_([level.id for level in levels])
        ).all()
        average_score = round(sum([data.score for data in student_levels]) / len(student_levels), 2) if student_levels else 0
        student_list.append({
            "name": student.full_name,
            "id": student.id,
            "average_score": average_score
        })
    
    # Ordenar la lista de estudiantes por promedio de menor a mayor
    student_list = sorted(student_list, key=lambda x: x["average_score"])

    return {
        "level_grades": level_grades,
        "level_times": level_times,
        "level_states": {
            "labels": level_states["labels"],
            "data": [
                {
                    "label": "Completados",
                    "data": [state["data"] for state in level_states["data"] if state["label"] == "Completados"],
                    "backgroundColor": COLORS[0]
                },
                {
                    "label": "Abandonados",
                    "data": [state["data"] for state in level_states["data"] if state["label"] == "Abandonados"],
                    "backgroundColor": COLORS[1]
                }
            ]
        },
        "story_states": {
            "labels": story_states["labels"],
            "data": [
                {
                    "label": "Completados",
                    "data": [state["data"] for state in story_states["data"] if state["label"] == "Completados"],
                    "backgroundColor": COLORS[2]
                },
                {
                    "label": "Abandonados",
                    "data": [state["data"] for state in story_states["data"] if state["label"] == "Abandonados"],
                    "backgroundColor": COLORS[3]
                }
            ]
        },
        "story_times": story_times,
        "student_list": student_list,
    }


@router.get("/get_kid_data")
def get_kid_data(
    player_id: int = Query(...),
    current_user: DashboardUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # Validar que el jugador existe
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Obtener datos del jugador y su representante
    caretaker = db.query(DashboardUser).join(CaretakerPlayer).filter(CaretakerPlayer.player_id == player_id).first()

    player_data = {
        "full_name": player.full_name,
        "age": player.edad,
        "ethnicity": player.ethnicity,
        "caretaker_name": caretaker.name if caretaker else "No asignado",
        "caretaker_email": caretaker.email if caretaker else "No asignado"
    }

    return player_data
@router.get("/get_kid_performance")
def get_kid_performance(
    player_id: int = Query(...),
    game_id: int = Query(...),
    current_user: DashboardUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # Validar que el jugador existe
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    level_grades = {"labels": [], "data": []}
    level_times = {"labels": [], "data": []}
    level_states = {"labels": [], "data": []}
    story_states = {"labels": [], "data": []}
    story_times = {"labels": [], "data": []}

    # Obtener todos los niveles asociados al juego
    levels = db.query(Level).join(Chapter).filter(Chapter.game_id == game_id).all()

    for level in levels:
        # Obtener todos los registros del jugador en ese nivel
        player_levels = db.query(PlayerLevel).filter(
            PlayerLevel.player_id == player_id,
            PlayerLevel.level_id == level.id
        ).all()

        if player_levels:
            # Calcular el promedio de las puntuaciones y tiempos
            avg_score = round(sum(data.score for data in player_levels) / len(player_levels), 2)
            avg_time = round(sum(data.total_time for data in player_levels) / len(player_levels), 2)
            completed = sum(1 for data in player_levels if data.state == "completed")
            abandoned = sum(1 for data in player_levels if data.state == "abandoned")

            level_grades["labels"].append(level.name)
            level_grades["data"].append(avg_score)
            level_times["labels"].append(level.name)
            level_times["data"].append(avg_time)

            level_states["labels"].append(level.name)
            level_states["data"].append({
                "label": "Completados",
                "data": completed
            })
            level_states["data"].append({
                "label": "Abandonados",
                "data": abandoned
            })

    # Obtener todas las historias asociadas al juego
    stories = db.query(Story).join(Chapter).filter(Chapter.game_id == game_id).all()

    for story in stories:
        # Obtener todos los registros del jugador en esa historia
        player_stories = db.query(PlayerStory).filter(
            PlayerStory.player_id == player_id,
            PlayerStory.story_id == story.id
        ).all()

        if player_stories:
            # Calcular el promedio de los tiempos vistos
            avg_time_watched = round(sum(data.time_watched for data in player_stories) / len(player_stories), 2)
            completed = sum(1 for data in player_stories if data.state == "completed")
            abandoned = sum(1 for data in player_stories if data.state == "abandoned")

            story_states["labels"].append(story.name)
            story_states["data"].append({
                "label": "Completados",
                "data": completed
            })
            story_states["data"].append({
                "label": "Abandonados",
                "data": abandoned
            })

            story_times["labels"].append(story.name)
            story_times["data"].append(avg_time_watched)

    return {
        "level_grades": level_grades,
        "level_times": level_times,
        "level_states": {
            "labels": level_states["labels"],
            "data": [
                {
                    "label": "Completados",
                    "data": [state["data"] for state in level_states["data"] if state["label"] == "Completados"],
                    "backgroundColor": COLORS[0]
                },
                {
                    "label": "Abandonados",
                    "data": [state["data"] for state in level_states["data"] if state["label"] == "Abandonados"],
                    "backgroundColor": COLORS[1]
                }
            ]
        },
        "story_states": {
            "labels": story_states["labels"],
            "data": [
                {
                    "label": "Completados",
                    "data": [state["data"] for state in story_states["data"] if state["label"] == "Completados"],
                    "backgroundColor": COLORS[2]
                },
                {
                    "label": "Abandonados",
                    "data": [state["data"] for state in story_states["data"] if state["label"] == "Abandonados"],
                    "backgroundColor": COLORS[3]
                }
            ]
        },
        "story_times": story_times
    }



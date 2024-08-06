# api/v1/endpoints/performance.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import date

from schemas.stage import StageBase
from schemas.educational_entity import EducationalEntityBase
from models import Stage, EducationalEntity, EducationReviewer, PlayerLevel, PlayerStory, Course, DashboardUser, Chapter, Player, Level, Story, CoursePlayer
from db.session import get_db
from utils.jwt_helper import get_current_user

router = APIRouter()

@router.get("/get_stages", response_model=List[StageBase])
def get_stages(db: Session = Depends(get_db)):
    stages = db.query(Stage).all()
    return stages

@router.get("/get_schools_admin", response_model=List[EducationalEntityBase])
def get_schools_admin(db: Session = Depends(get_db)):
    schools = db.query(EducationalEntity).all()
    return schools

@router.get("/get_schools_teacher", response_model=List[EducationalEntityBase])
def get_schools_teacher(current_user: DashboardUser = Depends(get_current_user), db: Session = Depends(get_db)):
    schools = db.query(EducationalEntity).join(EducationReviewer).filter(EducationReviewer.user_id == current_user.id).all()
    return schools

@router.get("/get_performance_school")
def get_performance_school(
    school_id: int,
    start_date: date,
    end_date: date,
    stage_id: int,
    game_id: int,
    current_user: DashboardUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # Obtención de capítulos y cálculo de promedios
    chapters = db.query(Chapter).filter(Chapter.game_id == game_id).all()
    charpter_grades = {"labels": [], "data": []}
    charpter_times = {"labels": [], "data": []}
    charpter_states = {"labels": [], "data": {"completed": [], "abandoned": []}}
    story_states = {"labels": [], "data": {"completed": [], "abandoned": []}}
    story_times = {"labels": [], "data": []}
    course_list = []

    for chapter in chapters:
        levels = db.query(Level).filter(Level.chapter_id == chapter.id).all()
        chapter_grades_data = []
        chapter_times_data = []
        chapter_completed = 0
        chapter_abandoned = 0
        for level in levels:
            level_data_query = db.query(PlayerLevel).filter(
                PlayerLevel.level_id == level.id,
                PlayerLevel.timestamp.between(start_date, end_date)
            )
            if current_user.role_id != 1:  # Si no es admin, filtrar por cursos del profesor
                level_data_query = level_data_query.join(Player).join(CoursePlayer).join(Course).filter(
                    Course.reviewer_id == current_user.id,
                    Course.educational_entity_id == school_id
                )
            level_data = level_data_query.all()
            scores = [data.score for data in level_data]
            times = [data.total_time for data in level_data]
            states = [data.state for data in level_data]
            chapter_grades_data.append(sum(scores) / len(scores) if scores else 0)
            chapter_times_data.append(sum(times) / len(times) if times else 0)
            chapter_completed += states.count('completed')
            chapter_abandoned += states.count('abandoned')
        charpter_grades["labels"].append(chapter.name)
        charpter_grades["data"].append(sum(chapter_grades_data) / len(chapter_grades_data) if chapter_grades_data else 0)
        charpter_times["labels"].append(chapter.name)
        charpter_times["data"].append(sum(chapter_times_data) / len(chapter_times_data) if chapter_times_data else 0)
        charpter_states["labels"].append(chapter.name)
        charpter_states["data"]["completed"].append(chapter_completed)
        charpter_states["data"]["abandoned"].append(chapter_abandoned)

        stories = db.query(Story).filter(Story.chapter_id == chapter.id).all()
        for story in stories:
            story_data_query = db.query(PlayerStory).filter(
                PlayerStory.story_id == story.id,
                PlayerStory.timestamp.between(start_date, end_date)
            )
            if current_user.role_id != 1:  # Si no es admin, filtrar por cursos del profesor
                story_data_query = story_data_query.join(Player).join(CoursePlayer).join(Course).filter(
                    Course.reviewer_id == current_user.id,
                    Course.educational_entity_id == school_id
                )
            story_data = story_data_query.all()
            story_states_data = {"completed": 0, "abandoned": 0}
            for data in story_data:
                if data.state == 'completed':
                    story_states_data["completed"] += 1
                else:
                    story_states_data["abandoned"] += 1
            story_states["labels"].append(story.name)
            story_states["data"]["completed"].append(story_states_data["completed"])
            story_states["data"]["abandoned"].append(story_states_data["abandoned"])
            story_times["labels"].append(story.name)
            story_times["data"].append(sum([data.time_watched for data in story_data]) / len(story_data) if story_data else 0)

    # Lista de cursos y sus promedios
    courses_query = db.query(Course).filter(Course.educational_entity_id == school_id, Course.game_id == game_id)
    if current_user.role_id != 1:  # Si no es admin, filtrar por cursos del profesor
        courses_query = courses_query.filter(Course.reviewer_id == current_user.id)
    courses = courses_query.all()
    for course in courses:
        course_students = db.query(PlayerLevel).join(Player).join(CoursePlayer).filter(
            CoursePlayer.course_id == course.id,
            PlayerLevel.timestamp.between(start_date, end_date)
        ).all()
        average_score = sum([data.score for data in course_students]) / len(course_students) if course_students else 0
        course_list.append({"name_curso": course.name, "id_curso": course.id, "promedio_curso_juego": average_score})

    return {
        "charpter_grades": charpter_grades,
        "charpter_times": charpter_times,
        "charpter_states": charpter_states,
        "story_states": story_states,
        "story_times": story_times,
        "Course_list": course_list,
    }

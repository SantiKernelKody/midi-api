from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.user_role import UserRole
from models.dashboard_user import DashboardUser
from models.educational_entity import EducationalEntity
from models.course import Course
from models.player import Player
from models.caretaker_player import CaretakerPlayer
from models.course_player import CoursePlayer
from models.education_reviewer import EducationReviewer
from models.player_level import PlayerLevel
from models.player_story import PlayerStory
from core.security import get_password_hash
from datetime import datetime

def seed():
    db: Session = SessionLocal()

    # Crear roles
    roles = [
        {"name": "admin", "display_name": "Administrator", "description": "Admin role"},
        {"name": "teacher", "display_name": "Teacher", "description": "Teacher role"},
        {"name": "parent", "display_name": "Parent", "description": "Parent role"}
    ]
    for role_data in roles:
        role = UserRole(**role_data)
        db.add(role)
    db.commit()

    admin_role = db.query(UserRole).filter_by(name="admin").first()
    teacher_role = db.query(UserRole).filter_by(name="teacher").first()
    parent_role = db.query(UserRole).filter_by(name="parent").first()

    # Crear usuarios
    users = [
        {
            "email": "admin@example.com",
            "password": get_password_hash("adminpassword"),
            "name": "Admin",
            "last_name": "User",
            "role_id": admin_role.id
        },
        {
            "email": "teacher1@example.com",
            "password": get_password_hash("teacherpassword1"),
            "name": "Teacher",
            "last_name": "One",
            "role_id": teacher_role.id
        },
        {
            "email": "teacher2@example.com",
            "password": get_password_hash("teacherpassword2"),
            "name": "Teacher",
            "last_name": "Two",
            "role_id": teacher_role.id
        },
        {
            "email": "parent1@example.com",
            "password": get_password_hash("parentpassword1"),
            "name": "Parent",
            "last_name": "One",
            "role_id": parent_role.id
        },
        {
            "email": "parent2@example.com",
            "password": get_password_hash("parentpassword2"),
            "name": "Parent",
            "last_name": "Two",
            "role_id": parent_role.id
        }
    ]
    for user_data in users:
        user = DashboardUser(**user_data)
        db.add(user)
    db.commit()

    # Crear escuelas
    schools = [
        {"name": "School One", "code": "SCH001", "description": "First school", "created_at": datetime.utcnow()},
        {"name": "School Two", "code": "SCH002", "description": "Second school", "created_at": datetime.utcnow()}
    ]
    for school_data in schools:
        school = EducationalEntity(**school_data)
        db.add(school)
    db.commit()

    school1 = db.query(EducationalEntity).filter_by(code="SCH001").first()
    school2 = db.query(EducationalEntity).filter_by(code="SCH002").first()

    teacher1 = db.query(DashboardUser).filter_by(email="teacher1@example.com").first()
    teacher2 = db.query(DashboardUser).filter_by(email="teacher2@example.com").first()

    # Asignar profesores a las escuelas
    education_reviewers = [
        {"education_id": school1.id, "reviewer_id": teacher1.id},
        {"education_id": school2.id, "reviewer_id": teacher1.id},
        {"education_id": school1.id, "reviewer_id": teacher2.id},
        {"education_id": school2.id, "reviewer_id": teacher2.id}
    ]
    for education_reviewer_data in education_reviewers:
        education_reviewer = EducationReviewer(**education_reviewer_data)
        db.add(education_reviewer)
    db.commit()

    # Crear cursos
    courses = [
        {"school_id": school1.id, "reviewer_id": teacher1.id, "subject_name": "Math 101", "description": "Math course 101"},
        {"school_id": school1.id, "reviewer_id": teacher1.id, "subject_name": "Science 101", "description": "Science course 101"},
        {"school_id": school2.id, "reviewer_id": teacher2.id, "subject_name": "Math 102", "description": "Math course 102"},
        {"school_id": school2.id, "reviewer_id": teacher2.id, "subject_name": "Science 102", "description": "Science course 102"}
    ]
    for course_data in courses:
        course = Course(**course_data)
        db.add(course)
    db.commit()

    course1 = db.query(Course).filter_by(subject_name="Math 101").first()
    course2 = db.query(Course).filter_by(subject_name="Science 101").first()
    course3 = db.query(Course).filter_by(subject_name="Math 102").first()
    course4 = db.query(Course).filter_by(subject_name="Science 102").first()

    # Crear jugadores y asignarlos a los cursos
    players = []
    for i in range(1, 6):
        players.append({"school_id": school1.id, "special_need_id": None, "full_name": f"Player {i} School 1", "edad": 10, "ethnicity": "Ethnicity 1", "special_need_description": None, "special_need": 0, "user_name": f"player{i}_s1", "password": get_password_hash("password")})
    for i in range(1, 6):
        players.append({"school_id": school2.id, "special_need_id": None, "full_name": f"Player {i} School 2", "edad": 11, "ethnicity": "Ethnicity 2", "special_need_description": None, "special_need": 0, "user_name": f"player{i}_s2", "password": get_password_hash("password")})

    for player_data in players:
        player = Player(**player_data)
        db.add(player)
    db.commit()

    # Asignar jugadores a los cursos
    for i in range(1, 6):
        player = db.query(Player).filter_by(user_name=f"player{i}_s1").first()
        course_player1 = CoursePlayer(course_id=course1.id, player_id=player.id)
        course_player2 = CoursePlayer(course_id=course2.id, player_id=player.id)
        db.add(course_player1)
        db.add(course_player2)
    for i in range(1, 6):
        player = db.query(Player).filter_by(user_name=f"player{i}_s2").first()
        course_player3 = CoursePlayer(course_id=course3.id, player_id=player.id)
        course_player4 = CoursePlayer(course_id=course4.id, player_id=player.id)
        db.add(course_player3)
        db.add(course_player4)
    db.commit()

    parent1 = db.query(DashboardUser).filter_by(email="parent1@example.com").first()
    parent2 = db.query(DashboardUser).filter_by(email="parent2@example.com").first()

    # Asignar padres a jugadores
    for i in range(1, 3):
        player = db.query(Player).filter_by(user_name=f"player{i}_s1").first()
        caretaker_player = CaretakerPlayer(representative_id=parent1.id, player_id=player.id)
        db.add(caretaker_player)
    for i in range(3, 6):
        player = db.query(Player).filter_by(user_name=f"player{i}_s2").first()
        caretaker_player = CaretakerPlayer(representative_id=parent2.id, player_id=player.id)
        db.add(caretaker_player)
    db.commit()

    # Crear juegos, capítulos y niveles
    game = {"name": "Math Game", "description": "A fun math game", "logo_game": "math_logo.png", "created_at": datetime.utcnow()}
    db_game = Game(**game)
    db.add(db_game)
    db.commit()

    chapter = {"game_id": db_game.id, "name": "Chapter 1", "description": "Introduction to Math", "created_at": datetime.utcnow()}
    db_chapter = Chapter(**chapter)
    db.add(db_chapter)
    db.commit()

    level = {"chapter_id": db_chapter.id, "name": "Level 1", "description": "Basic Math", "evaluation_criteria": "Score", "evaluation_method": "Points", "max_score": 100, "created_at": datetime.utcnow()}
    db_level = Level(**level)
    db.add(db_level)
    db.commit()

    story = {"chapter_id": db_chapter.id, "time": 10, "name": "Story 1", "description": "Math story", "created_at": datetime.utcnow()}
    db_story = Story(**story)
    db.add(db_story)
    db.commit()

    # Crear datos en player_level y player_story
    for i in range(1, 6):
        player = db.query(Player).filter_by(user_name=f"player{i}_s1").first()
        player_level = PlayerLevel(level_id=db_level.id, player_id=player.id, score=85.0, incorrect=5, correct=15, attempts=1, total_time=300, times_out_focus=2, created_at=datetime.utcnow())
        player_story = PlayerStory(story_id=db_story.id, player_id=player.id, time_watched=10, total_time_out=1, pauses=2, times_out_focus=1, created_at=datetime.utcnow())
        db.add(player_level)
        db.add(player_story)
    for i in range(1, 6):
        player = db.query(Player).filter_by(user_name=f"player{i}_s2").first()
        player_level = PlayerLevel(level_id=db_level.id, player_id=player.id, score=90.0, incorrect=3, correct=17, attempts=1, total_time=250, times_out_focus=1, created_at=datetime.utcnow())
        player_story = PlayerStory(story_id=db_story.id, player_id=player.id, time_watched=12, total_time_out=0, pauses=1, times_out_focus=1, created_at=datetime.utcnow())
        db.add(player_level)
        db.add(player_story)
    db.commit()

    db.close()

if __name__ == "__main__":
    seed()

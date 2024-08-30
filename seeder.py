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
from models.game import Game
from models.chapter import Chapter
from models.level import Level
from models.story import Story
from models.stage import Stage
from core.security import get_password_hash
from datetime import datetime
import random

def seed():
    db: Session = SessionLocal()

    # Crear roles
    roles = [
        {"name": "admin", "display_name": "Administrador", "description": "Rol de administrador"},
        {"name": "teacher", "display_name": "Profesor", "description": "Rol de profesor"},
        {"name": "parent", "display_name": "Padre", "description": "Rol de padre"}
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
            "email": "admin@ejemplo.com",
            "password": get_password_hash("contraseñaadmin"),
            "name": "Administrador",
            "last_name": "Usuario",
            "role_id": admin_role.id
        },
        {
            "email": "profesor@ejemplo.com",
            "password": get_password_hash("contraseñaprofesor"),
            "name": "Profesor",
            "last_name": "Usuario",
            "role_id": teacher_role.id
        },
        {
            "email": "padre@ejemplo.com",
            "password": get_password_hash("contraseñapadre"),
            "name": "Padre",
            "last_name": "Usuario",
            "role_id": parent_role.id
        }
    ]
    for user_data in users:
        user = DashboardUser(**user_data)
        db.add(user)
    db.commit()

    # Crear escuelas
    schools = [
        {"name": "Escuela Uno", "code": "ESC001", "description": "Primera escuela", "created_at": datetime.utcnow()},
        {"name": "Escuela Dos", "code": "ESC002", "description": "Segunda escuela", "created_at": datetime.utcnow()}
    ]
    for school_data in schools:
        school = EducationalEntity(**school_data)
        db.add(school)
    db.commit()

    school1 = db.query(EducationalEntity).filter_by(code="ESC001").first()
    school2 = db.query(EducationalEntity).filter_by(code="ESC002").first()

    teacher = db.query(DashboardUser).filter_by(email="profesor@ejemplo.com").first()
    parent = db.query(DashboardUser).filter_by(email="padre@ejemplo.com").first()

    # Asignar profesor a las escuelas
    education_reviewers = [
        {"education_id": school1.id, "reviewer_id": teacher.id},
        {"education_id": school2.id, "reviewer_id": teacher.id}
    ]
    for education_reviewer_data in education_reviewers:
        education_reviewer = EducationReviewer(**education_reviewer_data)
        db.add(education_reviewer)
    db.commit()

    # Crear cursos
    courses = [
        {"school_id": school1.id, "reviewer_id": teacher.id, "subject_name": "Matemáticas 101", "description": "Curso de matemáticas 101"},
        {"school_id": school1.id, "reviewer_id": teacher.id, "subject_name": "Ciencias 101", "description": "Curso de ciencias 101"},
        {"school_id": school2.id, "reviewer_id": teacher.id, "subject_name": "Matemáticas 102", "description": "Curso de matemáticas 102"},
        {"school_id": school2.id, "reviewer_id": teacher.id, "subject_name": "Ciencias 102", "description": "Curso de ciencias 102"}
    ]
    for course_data in courses:
        course = Course(**course_data)
        db.add(course)
    db.commit()

    courses = db.query(Course).all()

    # Crear etapas
    stages = [
        {"code": "R4", "name": "Etapa R4", "description": "Descripción para la etapa R4"},
        {"code": "R3", "name": "Etapa R3", "description": "Descripción para la etapa R3"},
        {"code": "R2", "name": "Etapa R2", "description": "Descripción para la etapa R2"},
        {"code": "R1", "name": "Etapa R1", "description": "Descripción para la etapa R1"},
        {"code": "R0", "name": "Etapa R0", "description": "Descripción para la etapa R0"},
        {"code": "Todos", "name": "Etapa Todos", "description": "Descripción para la etapa Todos"}
    ]
    for stage_data in stages:
        stage = Stage(**stage_data)
        db.add(stage)
    db.commit()

    stages = db.query(Stage).filter(Stage.code != 'Todos').all()

    # Crear jugadores y asignarlos a los cursos
    for i, course in enumerate(courses, start=1):
        for j in range(1, 11):
            player_data = {
                "school_id": course.school_id,
                "special_need_id": None,
                "full_name": f"Jugador {i}{j}",
                "edad": 10 + j % 2,
                "ethnicity": "Etnia",
                "special_need_description": None,
                "special_need": 0,
            }
            player = Player(**player_data)
            db.add(player)
            db.commit()

            course_player = CoursePlayer(course_id=course.id, player_id=player.id)
            db.add(course_player)
            db.commit()

            # Asociar padre con jugador1 y jugador2
            if j == 1 or j == 2:
                caretaker_player = CaretakerPlayer(representative_id=parent.id, player_id=player.id)
                db.add(caretaker_player)
                db.commit()

    # Crear juegos
    games = [
        {"name": "Juego Uno", "description": "Primer juego", "logo_game": "logo1.png", "created_at": datetime.utcnow()},
        {"name": "Juego Dos", "description": "Segundo juego", "logo_game": "logo2.png", "created_at": datetime.utcnow()}
    ]
    for game_data in games:
        game = Game(**game_data)
        db.add(game)
    db.commit()

    games = db.query(Game).all()

    # Crear capítulos, niveles e historias para cada juego
    for game in games:
        for i in range(1, 3):
            chapter_data = {"game_id": game.id, "name": f"Capítulo {i}", "description": f"Descripción del Capítulo {i}", "created_at": datetime.utcnow()}
            chapter = Chapter(**chapter_data)
            db.add(chapter)
            db.commit()

            level_data = {"chapter_id": chapter.id, "name": f"Nivel {i}", "description": f"Descripción del Nivel {i}", "evaluation_criteria": "Criterios", "evaluation_method": "Método", "max_score": 100, "created_at": datetime.utcnow()}
            level = Level(**level_data)
            db.add(level)
            db.commit()

            story_data = {"chapter_id": chapter.id, "time": 10, "name": f"Historia {i}", "description": f"Descripción de la Historia {i}", "created_at": datetime.utcnow()}
            story = Story(**story_data)
            db.add(story)
            db.commit()

            players = db.query(Player).all()
            for player in players:
                random_stage = random.choice(stages)

                player_level_data = {
                    "level_id": level.id,
                    "player_id": player.id,
                    "score": random.uniform(50.0, 100.0),
                    "incorrect": random.randint(0, 10),
                    "correct": random.randint(10, 20),
                    "attempts": random.randint(1, 3),
                    "total_time": random.randint(200, 400),
                    "times_out_focus": random.randint(0, 5),
                    "state": "completed" if random.choice([True, False]) else "abandoned",
                    "stage_id": random_stage.id,
                    "created_at": datetime.utcnow()
                }
                player_level = PlayerLevel(**player_level_data)
                db.add(player_level)
                db.commit()

                player_story_data = {
                    "story_id": story.id,
                    "player_id": player.id,
                    "time_watched": random.randint(5, 15),
                    "total_time_out": random.randint(0, 3),
                    "pauses": random.randint(1, 4),
                    "times_out_focus": random.randint(0, 3),
                    "state": "completed" if random.choice([True, False]) else "abandoned",
                    "stage_id": random_stage.id,
                    "created_at": datetime.utcnow()
                }
                player_story = PlayerStory(**player_story_data)
                db.add(player_story)
                db.commit()

    db.close()

if __name__ == "__main__":
    seed()

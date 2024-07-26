from sqlalchemy.orm import Session
from sqlalchemy import text
from db.session import SessionLocal
from models.user_role import UserRole
from models.dashboard_user import DashboardUser
from models.player import Player
from models.caretaker_player import CaretakerPlayer
from models.course import Course
from models.educational_entity import EducationalEntity
from models.course_player import CoursePlayer
from models.education_reviewer import EducationReviewer
from models.player_level import PlayerLevel
from models.player_story import PlayerStory
from models.game import Game
from models.chapter import Chapter
from models.level import Level
from models.story import Story

def reset_tables():
    db: Session = SessionLocal()

    # Reiniciar las tablas eliminando todos los registros
    db.query(PlayerStory).delete()
    db.query(PlayerLevel).delete()
    db.query(CoursePlayer).delete()
    db.query(CaretakerPlayer).delete()
    db.query(EducationReviewer).delete()
    db.query(Player).delete()
    db.query(Course).delete()
    db.query(EducationalEntity).delete()
    db.query(Story).delete()
    db.query(Level).delete()
    db.query(Chapter).delete()
    db.query(Game).delete()
    db.query(DashboardUser).delete()
    db.query(UserRole).delete()

    # Reiniciar contadores de ID (opcional, solo para PostgreSQL)
    db.execute(text("ALTER SEQUENCE dashboard_user_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE user_role_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE player_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE course_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE educational_entity_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE player_story_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE player_level_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE caretaker_player_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE course_player_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE education_reviewer_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE story_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE level_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE chapter_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE game_id_seq RESTART WITH 1"))

    db.commit()
    db.close()

if __name__ == "__main__":
    reset_tables()

# app/schemas/__init__.py
from .avatar import Avatar, AvatarCreate, AvatarUpdate
from .caretaker_player import CaretakerPlayer, CaretakerPlayerCreate, CaretakerPlayerUpdate
from .chapter import Chapter, ChapterCreate, ChapterUpdate
from .city import City, CityCreate, CityUpdate
from .course import Course, CourseCreate, CourseUpdate
from .course_player import CoursePlayer, CoursePlayerCreate, CoursePlayerUpdate
from .dashboard_user import DashboardUser, DashboardUserCreate, DashboardUserUpdate
from .educational_entity import EducationalEntity, EducationalEntityCreate, EducationalEntityUpdate
from .education_reviewer import EducationReviewer, EducationReviewerCreate, EducationReviewerUpdate
from .game import Game, GameCreate, GameUpdate
from .level import Level, LevelCreate, LevelUpdate
from .level_skills import LevelSkills, LevelSkillsCreate, LevelSkillsUpdate
from .player import Player, PlayerCreate, PlayerUpdate
from .player_level import PlayerLevel, PlayerLevelCreate, PlayerLevelUpdate
from .player_special_need import PlayerSpecialNeed, PlayerSpecialNeedCreate, PlayerSpecialNeedUpdate
from .player_story import PlayerStory, PlayerStoryCreate, PlayerStoryUpdate
from .politic_division import PoliticDivision, PoliticDivisionCreate, PoliticDivisionUpdate
from .room import Room, RoomCreate, RoomUpdate
from .skills import Skills, SkillsCreate, SkillsUpdate
from .special_need import SpecialNeed, SpecialNeedCreate, SpecialNeedUpdate
from .stage import Stage, StageCreate, StageUpdate
from .story import Story, StoryCreate, StoryUpdate
from .user_role import UserRole, UserRoleCreate, UserRoleUpdate
from .country import Country, CountryCreate, CountryUpdate
from .dashboard_user import DashboardUser, DashboardUserCreate
from .game_data import GameDataCreate
from .player import Player, PlayerCreate, PlayerUpdate
from .token import Token, TokenData
from .auth import LoginRequest

from math import ceil
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from requests import Session
from crud.user_role import is_admin
from db.session import get_db
from models.dashboard_user import DashboardUser as DashboardUserModel
from models.skills import Skills
from utils.jwt_helper import get_current_user
from schemas.skills import Skills as SkillSchema, SkillsCreate, SkillsUpdate
from models.game import Game as GameModel
from schemas.game import Game as GameSchema
from models.level import Level as LevelModel
from schemas.level import Level as LevelSchema, LevelUpdate, LevelWithSkillsSchema
from models.level_skills import LevelSkills as LevelSkillModel
from models.skills import Skills as SkillModel
from models.chapter import Chapter as ChapterModel
router = APIRouter()

@router.get("/skills", response_model=Dict[str, Any])
def get_skills(
    page: Optional[int] = Query(None, ge=1),
    size: Optional[int] = Query(None, ge=1),
    all: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):  # Verifica si es un usuario válido
        raise HTTPException(status_code=403, detail="Not authorized to access skills")

    if all:
        # Si el parámetro `all` es True, devolver todas las habilidades sin paginación
        skills = db.query(Skills).all()
        return {"skills": [SkillSchema.from_orm(skill) for skill in skills]}
    
    # Si no se solicita todas, manejar la paginación
    if page is None or size is None:
        raise HTTPException(status_code=400, detail="Page and size parameters are required unless `all` is True")

    offset = (page - 1) * size
    total_items = db.query(Skills).count()
    skills = db.query(Skills).offset(offset).limit(size).all()
    skills_schemas = [SkillSchema.from_orm(skill) for skill in skills]
    total_pages = ceil(total_items / size)

    return {
        "skills": skills_schemas,
        "total_items": total_items,
        "page": page,
        "size": size,
        "total_pages": total_pages
    }


@router.post("/create_skill", response_model=SkillSchema)
def create_skill(
    skill_data: SkillsCreate,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):  # Verifica si es un usuario válido
        raise HTTPException(status_code=403, detail="Not authorized to create skills")

    new_skill = Skills(name=skill_data.name, description=skill_data.description)
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill

@router.get("/skills/{skill_id}", response_model=SkillSchema)
def get_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to access skill details")

    # Obtener la skill por ID
    skill = db.query(SkillModel).filter(SkillModel.id == skill_id).first()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    return skill

@router.put("/skills/{skill_id}", response_model=SkillSchema)
def update_skill(
    skill_id: int,
    skill_data: SkillsUpdate,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):  # Verifica si es un usuario válido
        raise HTTPException(status_code=403, detail="Not authorized to update skills")

    skill = db.query(Skills).filter(Skills.id == skill_id).first()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    skill.name = skill_data.name
    skill.description = skill_data.description

    db.commit()
    db.refresh(skill)

    return skill

@router.delete("/skills/{skill_id}", response_model=dict)
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):  # Verifica si es un usuario válido
        raise HTTPException(status_code=403, detail="Not authorized to delete skills")

    skill = db.query(Skills).filter(Skills.id == skill_id).first()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(skill)
    db.commit()

    return {"message": "Skill deleted successfully"}

@router.get("/games", response_model=Dict[str, Any])
def get_games(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):  # Verifica si es un usuario válido
        raise HTTPException(status_code=403, detail="Not authorized to access games")

    offset = (page - 1) * size
    total_items = db.query(GameModel).count()
    games = db.query(GameModel).offset(offset).limit(size).all()

    games_schemas = [GameSchema.from_orm(game) for game in games]
    total_pages = ceil(total_items / size)

    return {
        "games": games_schemas,
        "total_items": total_items,
        "page": page,
        "size": size,
        "total_pages": total_pages
    }

@router.get("/game/{game_id}/levels", response_model=Dict[str, Any])
def get_levels_for_game(
    game_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):  # Verifica si es un usuario autorizado
        raise HTTPException(status_code=403, detail="Not authorized to access levels")

    offset = (page - 1) * size
    
    # Contar el número total de niveles para el juego dado
    total_items = db.query(LevelModel).join(ChapterModel, LevelModel.chapter_id == ChapterModel.id)\
        .filter(ChapterModel.game_id == game_id).count()
    
    # Obtener los niveles asociados con el juego dado, manejando la paginación
    levels = db.query(LevelModel).join(ChapterModel, LevelModel.chapter_id == ChapterModel.id)\
        .filter(ChapterModel.game_id == game_id).offset(offset).limit(size).all()

    if not levels:
        raise HTTPException(status_code=404, detail="No levels found for the given game")

    # Convertir la lista de niveles obtenidos a esquemas Pydantic
    levels_schemas = [LevelSchema.from_orm(level) for level in levels]
    total_pages = ceil(total_items / size)

    return {
        "levels": levels_schemas,
        "total_items": total_items,
        "page": page,
        "size": size,
        "total_pages": total_pages
    }

@router.get("/level/{level_id}", response_model=LevelWithSkillsSchema)
def get_level_with_skills(
    level_id: int,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to access level details")

    # Obtener el nivel por ID
    level = db.query(LevelModel).filter(LevelModel.id == level_id).first()

    if not level:
        raise HTTPException(status_code=404, detail="Level not found")

    # Obtener las relaciones de skills que aún existen y están asociadas con el nivel
    existing_skill_ids = (
        db.query(LevelSkillModel.skill_id)
        .join(SkillModel, SkillModel.id == LevelSkillModel.skill_id)
        .filter(LevelSkillModel.level_id == level_id, SkillModel.id.isnot(None))
        .all()
    )
    
    # Convertir los resultados a una lista simple de IDs
    existing_skill_ids = [skill_id[0] for skill_id in existing_skill_ids]

    # Crear el esquema de respuesta
    level_with_skills = LevelWithSkillsSchema(
        id=level.id,
        name=level.name,
        description=level.description,
        evaluation_criteria=level.evaluation_criteria,
        max_score=level.max_score,
        skill_ids=existing_skill_ids
    )

    return level_with_skills

@router.put("/level/{level_id}", response_model=dict)
def update_level(
    level_id: int,
    level_data: LevelUpdate,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to update levels")

    # Obtener el nivel a actualizar
    level = db.query(LevelModel).filter(LevelModel.id == level_id).first()

    if not level:
        raise HTTPException(status_code=404, detail="Level not found")

    # Actualizar los datos del nivel
    level.name = level_data.name
    level.description = level_data.description
    level.evaluation_criteria = level_data.evaluation_criteria
    level.max_score = level_data.max_score
    db.commit()

    # Eliminar todas las relaciones actuales de skills en level_skills
    db.query(LevelSkillModel).filter(LevelSkillModel.level_id == level_id).delete()
    db.commit()

    # Crear nuevas relaciones con los skills_ids proporcionados
    for skill_id in level_data.skill_ids:
        skill = db.query(SkillModel).filter(SkillModel.id == skill_id).first()
        if skill:
            level_skill = LevelSkillModel(level_id=level_id, skill_id=skill_id)
            db.add(level_skill)
    
    db.commit()

    return {"message": "Level updated successfully"}
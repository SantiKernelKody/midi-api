from sqlalchemy.orm import Session
from models.educational_entity import EducationalEntity
from schemas.educational_entity import EducationalEntityCreate, EducationalEntityUpdate

def get_educational_entity_by_code(db: Session, code: str):
    return db.query(EducationalEntity).filter(EducationalEntity.code == code).first()

def get_educational_entity(db: Session, entity_id: int):
    return db.query(EducationalEntity).filter(EducationalEntity.id == entity_id).first()

def get_educational_entities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EducationalEntity).offset(skip).limit(limit).all()

def create_educational_entity(db: Session, educational_entity: EducationalEntityCreate):
    db_educational_entity = EducationalEntity(**educational_entity.dict())
    db.add(db_educational_entity)
    db.commit()
    db.refresh(db_educational_entity)
    return db_educational_entity

def update_educational_entity(db: Session, entity_id: int, educational_entity: EducationalEntityUpdate):
    db_educational_entity = db.query(EducationalEntity).filter(EducationalEntity.id == entity_id).first()
    if db_educational_entity is None:
        return None
    for key, value in educational_entity.dict(exclude_unset=True).items():
        setattr(db_educational_entity, key, value)
    db.commit()
    db.refresh(db_educational_entity)
    return db_educational_entity

def delete_educational_entity(db: Session, entity_id: int):
    db_educational_entity = db.query(EducationalEntity).filter(EducationalEntity.id == entity_id).first()
    if db_educational_entity is None:
        return None
    db.delete(db_educational_entity)
    db.commit()
    return db_educational_entity

from pydantic import BaseModel

class LevelSkillsBase(BaseModel):
    level_id: int
    skill_id: int

class LevelSkillsCreate(LevelSkillsBase):
    pass

class LevelSkillsUpdate(LevelSkillsBase):
    pass

class LevelSkillsInDBBase(LevelSkillsBase):
    id: int

    class Config:
        orm_mode = True

class LevelSkills(LevelSkillsInDBBase):
    pass

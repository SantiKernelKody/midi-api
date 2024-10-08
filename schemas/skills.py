from pydantic import BaseModel

class SkillsBase(BaseModel):
    name: str
    description: str

class SkillsCreate(SkillsBase):
    pass

class SkillsUpdate(SkillsBase):
    pass

class SkillsInDBBase(SkillsBase):
    id: int

    class Config:
        orm_mode = True

class Skills(SkillsInDBBase):
    pass

class SkillsInDB(SkillsInDBBase):
    pass

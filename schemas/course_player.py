from pydantic import BaseModel

class CoursePlayerBase(BaseModel):
    course_id: int
    player_id: int

class CoursePlayerCreate(CoursePlayerBase):
    pass

class CoursePlayerUpdate(CoursePlayerBase):
    pass

class CoursePlayerInDBBase(CoursePlayerBase):
    id: int

    class Config:
        orm_mode = True

class CoursePlayer(CoursePlayerInDBBase):
    pass

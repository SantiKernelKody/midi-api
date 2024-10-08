from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    subject_name: str
    description: str

class CourseCreate(CourseBase):
    school_id: int
    reviewer_id: int

class CourseUpdate(CourseBase):
    school_id: Optional[int] = None
    reviewer_id: Optional[int] = None

class CourseInDBBase(CourseBase):
    #id: int
    school_id: int
    reviewer_id: int

    class Config:
        orm_mode = True

class Course(CourseInDBBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True
    pass

class CourseInDB(CourseInDBBase):
    pass

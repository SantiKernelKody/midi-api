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
    id: int
    school_id: int
    reviewer_id: int

    class Config:
         from_attributes = True

class Course(CourseInDBBase):
    pass

class CourseInDB(CourseInDBBase):
    pass

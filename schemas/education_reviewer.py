from pydantic import BaseModel

class EducationReviewerBase(BaseModel):
    education_id: int
    reviewer_id: int

class EducationReviewerCreate(EducationReviewerBase):
    pass

class EducationReviewerUpdate(EducationReviewerBase):
    pass

class EducationReviewerInDBBase(EducationReviewerBase):
    id: int

    class Config:
        orm_mode = True

class EducationReviewer(EducationReviewerInDBBase):
    pass

from pydantic import BaseModel


class ProgressCreate(BaseModel):
    weight: float
    height: float


class ProgressResponse(BaseModel):
    id: int
    weight: float
    height: float
    bmi: float
    user_id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel

class WorkoutCreate(BaseModel):
    workout_name: str
    duration: int
    calories_burned: int


class WorkoutResponse(BaseModel):
    id: int
    workout_name: str
    duration: int
    calories_burned: int

    class Config:
        from_attributes = True
from pydantic import BaseModel


class NutritionCreate(BaseModel):
    food_name: str
    calories: int
    protein: float
    carbs: float


class NutritionResponse(BaseModel):
    id: int
    food_name: str
    calories: int
    protein: float
    carbs: float
    user_id: int

    class Config:
        from_attributes = True

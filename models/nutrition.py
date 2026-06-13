from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Nutrition(Base):

    __tablename__ = "nutrition"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    food_name: Mapped[str] = mapped_column(String)

    calories: Mapped[int] = mapped_column(Integer)

    protein: Mapped[float] = mapped_column(Float)

    carbs: Mapped[float] = mapped_column(Float)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
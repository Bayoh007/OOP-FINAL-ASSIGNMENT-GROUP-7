from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Workout(Base):

    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    workout_name: Mapped[str] = mapped_column(String)

    duration: Mapped[int] = mapped_column(Integer)

    calories_burned: Mapped[int] = mapped_column(Integer)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
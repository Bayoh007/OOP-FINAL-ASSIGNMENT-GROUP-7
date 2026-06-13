from sqlalchemy import Column, Integer, Float, ForeignKey

from database.database import Base


class Progress(Base):

    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)

    weight = Column(Float)

    height = Column(Float)

    bmi = Column(Float)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )
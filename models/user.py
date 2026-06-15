from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    fullname: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    password: Mapped[str] = mapped_column(String)
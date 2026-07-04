from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from app.infostructure.db.sqlite.base import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    disk_space: Mapped[int] = mapped_column(default=10*pow(1024, 3))
    used_space: Mapped[int] = mapped_column(default=0)
    hashed_password: Mapped[str]




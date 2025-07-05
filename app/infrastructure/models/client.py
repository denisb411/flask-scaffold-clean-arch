from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.models.base_model import Base

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

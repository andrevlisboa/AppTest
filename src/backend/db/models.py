from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    main_dishes = relationship("MainDish", back_populates="user")


class MainDish(Base):
    __tablename__ = "main_dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="main_dishes")

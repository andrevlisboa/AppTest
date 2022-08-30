from typing import List

from pydantic import BaseModel


class MainDishBase(BaseModel):
    name: str
    type: str


class MainDishCreate(MainDishBase):
    pass


class MainDish(MainDishBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    main_dishes: List[MainDish] = []

    class Config:
        orm_mode = True

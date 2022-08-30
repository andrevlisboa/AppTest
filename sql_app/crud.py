from sqlalchemy.orm import Session

from . import models, schemas

# USER
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session):
    skip = 0
    limit = 100
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# MAIN DISHES
def get_main_dishes(db: Session):
    skip = 0
    limit = 100
    return db.query(models.MainDish).offset(skip).limit(limit).all()


def get_main_dish_by_id(db: Session, user_id: int):
    skip = 0
    limit = 100
    return db.query(models.MainDish).filter(models.MainDish.user_id == user_id).offset(skip).limit(limit).all()


def get_user_main_dishes_by_type(db: Session, user_id: int, type: str):
    skip = 0
    limit = 100
    return db.query(models.MainDish).filter(models.MainDish.type == type, models.MainDish.user_id == user_id).offset(skip).limit(limit).all()

def get_user_main_dishes_by_id(db: Session, user_id: int, main_dish_id: int):
    return db.query(models.MainDish).filter(models.MainDish.id == main_dish_id, models.MainDish.user_id == user_id).first()


def create_user_main_dish(db: Session, main_dish: schemas.MainDishCreate, user_id: int):
    db_item = models.MainDish(**main_dish.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_user_main_dish(db: Session, main_dish_id: int):
    db_item = db.get(models.MainDish, main_dish_id)
    db.delete(db_item)
    db.commit()
    return db_item

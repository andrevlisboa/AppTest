from typing import List
from pydantic import conlist

from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from .. import crud, models, schemas
from .database import SessionLocal, engine

import os

models.Base.metadata.create_all(bind=engine)
IMAGEDIR = "images/"
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# vue 
@app.get("/app")
def read_index():
    return FileResponse("../frontend/app.html")

##
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_all_users(db: Session = Depends(get_db)) -> dict:
    users = crud.get_users(db)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/main_dishes/", response_model=List[schemas.MainDish])
def read_all_main_dishes(db: Session = Depends(get_db)) -> dict:
    main_dishes = crud.get_main_dishes(db)
    return main_dishes


@app.post("/users/{user_id}/main_dishes/", response_model=schemas.MainDish)
async def create_main_dish_for_user(
        user_id: int, item: schemas.MainDishCreate, db: Session = Depends(get_db)
):
    return crud.create_user_main_dish(db=db, main_dish=item, user_id=user_id)


@app.get("/users/{user_id}/main_dishes/", response_model=List[schemas.MainDish])
def read_user_main_dishes(user_id: int, db: Session = Depends(get_db)):
    main_dish = crud.get_main_dish_by_id(db, user_id=user_id)
    return main_dish

@app.get("/users/{user_id}/main_dishes/{type}", response_model=List[schemas.MainDish])
def read_user_main_dishes_by_type(user_id: int, type: str, db: Session = Depends(get_db)) -> dict:
    main_dish = crud.get_user_main_dishes_by_type(db, type=type, user_id=user_id)
    return main_dish


@app.post("/users/{user_id}/main_dishes/{main_dish_id}/image/")
async def create_main_dish_image(png_image: UploadFile, main_dish_id: int, user_id: int):
    png_image.filename = f"{user_id}_{main_dish_id}.png"
    contents = await png_image.read()  # <-- Important!
    with open(f"{IMAGEDIR}{png_image.filename}", "wb") as f:
        f.write(contents)

    return {"ok": True}


@app.get("/users/{user_id}/main_dishes/{main_dish_id}/image/", response_class=FileResponse)
async def read_main_dish_image(main_dish_id: int, user_id: int) -> dict:
    try:
        file_name = f"{user_id}_{main_dish_id}.png"
        path = f"{IMAGEDIR}{file_name}"
        return path
    except:
        raise HTTPException(status_code=400, detail="Image not found")

@app.post("/users/{user_id}/menu")
def get_user_menu(user_id: int, main_dishes_ids: conlist(int), db: Session = Depends(get_db)):

    text = f"Estes são os pratos:"

    for main_dish_id in main_dishes_ids:
        main_dish = crud.get_user_main_dishes_by_id(db, user_id=user_id, main_dish_id=main_dish_id)

        if main_dish_id !=main_dishes_ids[-1]:
            text += f"{main_dish.name},"
        else:
            text += f"{main_dish.name}."

    return text


@app.delete("/users/{user_id}/main_dishes/{main_dish_id}/image")
async def delete_main_dish_image(main_dish_id: int, user_id: int):
    try:
        file_name = f"{user_id}_{main_dish_id}.png"
        path = f"{IMAGEDIR}{file_name}"
        print(path)
        os.remove(path)
        return {"ok": True}
    except:
        raise HTTPException(status_code=404, detail="Main Dish Image not found")



@app.delete("/users/{user_id}/main_dishes/{main_dish_id}")
async def delete_main_dish(main_dish_id: int,  db: Session = Depends(get_db)):
    try:
        crud.delete_user_main_dish(db, main_dish_id=main_dish_id)
        return {"ok": True}
    except:
        raise HTTPException(status_code=404, detail="Main Dish not found")





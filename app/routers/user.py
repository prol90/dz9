from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db_depends import get_db
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import select, insert, update, delete

from typing import List

router = APIRouter()


@router.get("/", response_model=List[CreateUser])
def all_users(db: Session = Depends(get_db)):
    users = db.scalars(select(User)).all()
    return users


@router.get("/{user_id}", response_model=CreateUser)
def user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    for key, value in user.dict().items():
        setattr(db_user, key, value)

    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}


@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.delete(db_user)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User deletion is successful!"}

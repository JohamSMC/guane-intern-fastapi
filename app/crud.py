from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import True_
from sqlalchemy.sql.functions import user
from fastapi import status
import requests

from app import models, schemas

def getRandomImageUrl():
    """Function that returns a URL of a random dog image(https://dog.ceo/api/breeds/image/random)
    or the status code if the request response is different from 200_OK

    Returns:
        [string]: [URL o status code ]
    """
    req = requests.get("https://dog.ceo/api/breeds/image/random")
    if req.status_code == status.HTTP_200_OK:
        return req.json()["message"]
    else:
        return str(req.status_code)


# -----------CRUD DOGS-----------
def get_dogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dog).offset(skip).limit(limit).all()


def get_dog_by_name(db: Session, dog_name: str):
    return db.query(models.Dog).filter(models.Dog.name == dog_name).first()


def get_dogs_is_adopted(db: Session):
    return db.query(models.Dog).filter(models.Dog.is_adopted == True).all()


def create_dog(db: Session, dog: schemas.DogCreate):
    db_dog = models.Dog(**dog.dict(), picture=getRandomImageUrl(), create_date=str(datetime.utcnow()))
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    return db_dog


def update_dog(db: Session, dog_name: str, dog: schemas.DogCreate):
    db.query(models.Dog).filter(models.Dog.name == dog_name).update({"name":dog.name,
                                                                    "is_adopted":dog.is_adopted,
                                                                    "id_user":dog.id_user},
                                                                    synchronize_session=False)
    db.commit()
    return db.query(models.Dog).filter(models.Dog.name == dog.name).first()


def delete_dog(db: Session, dog_name: str):
    db.query(models.Dog).filter(models.Dog.name == dog_name).delete(synchronize_session=False)
    db.commit()


# -----------CRUD USERS-----------
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_email: str, user: schemas.UserCreate):
    db.query(models.User).filter(models.User.email == user_email).update({"first_name":user.first_name,
                                                                    "last_name":user.last_name,
                                                                    "email":user.email,
                                                                    "hashed_password":user.hashed_password,
                                                                    "is_active":user.is_active},
                                                                    synchronize_session=False)
    db.commit()
    return db.query(models.User).filter(models.User.email == user.email).first()


def delete_user(db: Session, user_email: str):
    db.query(models.User).filter(models.User.email == user_email).delete(synchronize_session=False)
    db.commit()
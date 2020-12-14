from os import name
from typing import List
from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=" APIT REST Backend technical testing",
    description="Designing a API REST with the python FastAPI framework"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"TEST": "Successfully"}


# ---------------------API ENDPOINT DOGS------------------------------------

# ---------------------ENDPOINTS GET DOGS-----------------------------------
@app.get("/api/dogs/", response_model=List[schemas.Dog])
def read_dogs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_dogs = crud.get_dogs(db=db, skip=skip, limit=limit)
    return db_dogs


@app.get("/api/dogs/{dog_name}", response_model=schemas.Dog)
def read_dog_by_name(dog_name: str, db: Session = Depends(get_db)):
    db_dog = crud.get_dog_by_name(db=db, dog_name=dog_name)
    if db_dog is None:
        raise HTTPException(status_code=404,
                            detail=f'DOG with NAME:"{dog_name}" DOES NO EXIST')
    return db_dog


@app.get("/api/dogs/is_adopted/", response_model=List[schemas.Dog])
def read_dogs_is_adopted(db: Session = Depends(get_db)):
    db_dogs_is_adopted = crud.get_dogs_is_adopted(db=db)
    if db_dogs_is_adopted is None:
        raise HTTPException(status_code=404, detail="There are no dogs that 'IS ADOPTED'")
    return db_dogs_is_adopted


# ---------------------ENDPOINTS POST DOGS-----------------------------------
@app.post("/api/dogs/", response_model=schemas.Dog)
def create_dog(dog: schemas.DogCreate, db: Session = Depends(get_db)):
    db_dog = crud.get_dog_by_name(db=db, dog_name=dog.name)
    if db_dog:
        raise HTTPException(status_code=400,
                            detail=f'DOG with NAME:"{dog.name}" ready registered')
    else:
        db_user_dog = crud.get_user_by_id(db=db, user_id=dog.id_user)
        if db_user_dog:
            return crud.create_dog(db=db, dog=dog)
        else:
            raise HTTPException(status_code=404,
                                detail=f'USER with ID:"{dog.id_user}"DOES NO EXIST\
                                        and therefore CAN NOT BE CREATE the DOG with NAME:"{dog.name}"')


# ---------------------ENDPOINTS PUT DOGS-----------------------------------
@app.put("/api/dogs/{dog_name}", response_model=schemas.Dog)
def update_dog(dog_name: str, payload: schemas.DogCreate, db: Session = Depends(get_db)):
    db_dog = crud.get_dog_by_name(db=db, dog_name=dog_name)
    if db_dog:
        db_user_dog = crud.get_user_by_id(db=db, user_id=payload.id_user)
        if db_user_dog:
            return crud.update_dog(db=db, dog_name=dog_name, dog=payload)
        else:
            raise HTTPException(status_code=404,
                                detail=f'USER with ID:"{payload.id_user}"DOES NO EXIST\
                                        and therefore CAN NOT BE UPDATE the DOG with NAME:"{dog_name}"')
    else:
        raise HTTPException(status_code=404,
                            detail=f'DOG with NAME:"{dog_name}" DOES NO EXIST\
                                    and therefore CAN NOT BE UPDATE')


# ---------------------ENDPOINTS DELETE DOGS-----------------------------------
@app.delete("/api/dogs/{dog_name}", status_code=status.HTTP_200_OK)
def delete_dog(dog_name: str, db: Session = Depends(get_db)):
    db_dog = crud.get_dog_by_name(db=db, dog_name=dog_name)
    if db_dog:
        crud.delete_dog(db=db, dog_name=dog_name)
        return {"message": f'Dog with name:"{dog_name}" deleted successfully!'}
    else:
        raise HTTPException(status_code=404,
                            detail=f'DOG with NAME:"{dog_name}" DOES NO EXIST\
                                    and therefore CAN NOT BE DELETE')


# ---------------------API ENDPOINT USERS------------------------------------

# ---------------------ENDPOINTS GET USERS-----------------------------------
@app.get("/api/users/", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_users = crud.get_users(db=db, skip=skip, limit=limit)
    return db_users


@app.get("/api/user/{user_email}", response_model=schemas.User)
def read_user_by_email(user_email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, user_email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404,
                            detail=f'USER with EMAIL:"{user_email}" DOES NO EXIST')
    return db_user


# ---------------------ENDPOINTS POST USERS-----------------------------------
@app.post("/api/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, user_email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail=f'USER with EMAIL:"{user.email}" ready registered')
    return crud.create_user(db=db, user=user)


# ---------------------ENDPOINTS PUT USERS-----------------------------------
@app.put("/api/user/{user_email}", response_model=schemas.User, status_code=status.HTTP_200_OK)
def update_user(user_email: str, payload: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, user_email=user_email)
    if db_user:
        return crud.update_user(db=db, user_email=user_email, user=payload)
    else:
        raise HTTPException(
            status_code=404, detail=f'USER with EMAIL:"{user_email}" DOES NO EXIST\
                                    and therefore CAN NOT BE UPDATE')


# ---------------------ENDPOINTS DELETE USERS-----------------------------------
@app.delete("/api/user/{user_email}", status_code=status.HTTP_200_OK)
def delete_user(user_email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, user_email=user_email)
    if db_user:
        crud.delete_user(db=db, user_email=user_email)
        return {"message": f'User with EMAIL:"{user_email}" deleted successfully!'}
    else:
        raise HTTPException(
            status_code=404, detail=f'USER with EMAIL:"{user_email}" DOES NO EXIST\
                                    and therefore CAN NOT BE DELETE')

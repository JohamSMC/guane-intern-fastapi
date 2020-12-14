from typing import List, Optional
from pydantic import BaseModel

# --------SCHEMAS DOG--------
class DogBase(BaseModel):
    name: str
    is_adopted: bool
    id_user: int


class DogCreate(DogBase):
    pass


class Dog(DogBase):
    id: int
    picture: str
    create_date: str

    class Config:
        orm_mode = True


# --------SCHEMAS USER--------
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    hashed_password: str
    is_active: bool


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    dogs: List[Dog] = []

    class Config:
        orm_mode = True

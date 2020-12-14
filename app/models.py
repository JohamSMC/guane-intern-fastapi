from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


# ----------MODEL USER----------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    dogs = relationship("Dog",
                        back_populates="owner",
                        cascade="all, delete",
                        passive_deletes=True)


# ----------MODEL DOG----------
class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    picture = Column(String, index=True)
    create_date = Column(String, index=True)
    is_adopted = Column(Boolean, default=False)
    id_user = Column(Integer, ForeignKey("users.id",
                                        ondelete="CASCADE"))

    owner = relationship("User", back_populates="dogs")

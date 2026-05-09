from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
from database import engine
import uuid
from sqlalchemy import DateTime
from datetime import datetime

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String, unique=True)
    password = Column(String)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    description = Column(String)
    user_id = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime , nullable=True)



# create table
Base.metadata.create_all(bind=engine)


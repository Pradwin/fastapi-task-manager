from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    name: str
    age: int
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: str
    status:str = "pending"
    due_date: datetime | None = None

class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str 
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status:str
    created_at: datetime
    due_date: datetime | None = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: str
    name: str
    age: int
    email: str

    class Config:
        from_attributes = True



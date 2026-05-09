from fastapi import APIRouter,HTTPException,Depends
from database import get_db
from sqlalchemy.orm import Session
from Schemas.schemas import User,UserResponse,LoginRequest
from Crud import UserCrud
from Utils.Security import verify_password
from Utils.Jwt_handler import create_token
from Models.models import UserDB
from Utils.Dependencies import get_current_user

router = APIRouter()

@router.post("/login",status_code=201)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_token({"sub": db_user.email})

    return {"access_token": token}

@router.post("/signup",response_model=UserResponse,status_code=201)
def create_user(user: User,db: Session = Depends(get_db)):
    return UserCrud.create_user(db, user)


@router.get("/", response_model=UserResponse,status_code=200)
def get_users(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return UserCrud.get_users(db,current_user)


@router.put("/{user_id}",response_model=UserResponse,status_code=201)
def update_user(user_id: str, user: User,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    result = UserCrud.update_user(db, user_id, user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return result


@router.delete("/{user_id}",status_code=204)
def delete_user(user_id: str,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    result = UserCrud.delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted"}








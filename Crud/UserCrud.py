from Models.models import UserDB
from Utils.Security import hash_password
from fastapi import HTTPException
from Utils.Logging import logger


def create_user(db, user):
    hashed_pwd = hash_password(user.password)

    new_user = UserDB(
        name=user.name,
        age=user.age,
        email=user.email,
        password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User Created: {user.email}")

    return new_user


def get_users(db,current_user):
    users = db.query(UserDB).filter(UserDB.id == current_user.id).one()
    return users


def update_user(db,user_id,user):

    existing_user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # update fields
    existing_user.name = user.name
    existing_user.age = user.age
    existing_user.email = user.email

    db.commit()
    db.refresh(existing_user)
    logger.info(f"User Updated: {user.email}")

    return existing_user


def delete_user(db,user_id):

    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User doesn't Exist")

    db.delete(user)
    db.commit()
    logger.warning(f"User Deleted: {user.email}")

    return user
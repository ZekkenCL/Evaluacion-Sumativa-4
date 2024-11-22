from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        surname=user.surname,
        password=models.User.get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: str):
    db_user = db.query(models.User).filter(models.User.id == user_id, models.User.is_deleted == False).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def get_user_by_email(db: Session, email: str):
    """
    Obtiene un usuario por su correo electrónico.
    """
    db_user = db.query(models.User).filter(models.User.email == email, models.User.is_deleted == False).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).filter(models.User.is_deleted == False).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: str, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.is_deleted = True
    db.commit()
    return db_user

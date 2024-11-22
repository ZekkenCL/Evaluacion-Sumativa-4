from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, models, schemas, database, auth, seeders
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta








models.Base.metadata.create_all(bind=database.engine)


def populate_db(db: Session):
    if db.query(models.User).count() == 0:
        seeders.seed_users(db, num_users=51) 

populate_db(database.SessionLocal())


app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db=db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.UserInDB)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), token: str = Depends(auth.get_current_user)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.UserInDB)
def read_user(user_id: str, db: Session = Depends(get_db), token: str = Depends(auth.get_current_user)):
    return crud.get_user(db=db, user_id=user_id)

@app.get("/users/", response_model=list[schemas.UserInDB])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: str = Depends(auth.get_current_user)):
    return crud.get_users(db=db, skip=skip, limit=limit)

@app.patch("/users/{user_id}", response_model=schemas.UserInDB)
def update_user(user_id: str, user: schemas.UserUpdate, db: Session = Depends(get_db), token: str = Depends(auth.get_current_user)):
    return crud.update_user(db=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}", response_model=schemas.UserInDB)
def delete_user(user_id: str, db: Session = Depends(get_db), token: str = Depends(auth.get_current_user)):
    return crud.delete_user(db=db, user_id=user_id)

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas, database, auth, seeders

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

@app.post("/users/", response_model=schemas.UserInDB)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.UserInDB)
def read_user(user_id: str, db: Session = Depends(get_db)):
    return crud.get_user(db=db, user_id=user_id)

@app.get("/users/", response_model=list[schemas.UserInDB])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)

@app.patch("/users/{user_id}", response_model=schemas.UserInDB)
def update_user(user_id: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}", response_model=schemas.UserInDB)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)

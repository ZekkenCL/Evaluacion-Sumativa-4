from sqlalchemy.orm import Session
from . import models
from faker import Faker

fake = Faker()

FIXED_USER = {
    "name": "Admin",
    "surname": "User",
    "email": "admin@example.com",
    "password": "password123"
}

def create_user(db: Session, name: str, surname: str, email: str, password: str):
    user = models.User(
        name=name,
        email=email,
        surname=surname,
        password=models.User.get_password_hash(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_fixed_user(db: Session):
    create_user(db, **FIXED_USER)

def create_fake_users(db: Session, num_users: int = 51):
    current_user_count = db.query(models.User).count()
    if current_user_count < num_users:
        for _ in range(num_users - current_user_count):
            name = fake.first_name()
            surname = fake.last_name()
            email = fake.email()
            password = "password123"
            create_user(db, name, surname, email, password)

def seed_users(db: Session, num_users: int = 51):
    create_fixed_user(db)
    create_fake_users(db, num_users)

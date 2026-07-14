from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import hash_password, verify_password
from app.schemas.error import Error


def get_user_by_email(db: Session, email: str) -> User | None:
    return (
        db.query(User)
        .filter(User.email==email)
        .first()
    )


def create_user(db: Session, user: UserCreate) -> User | Error:

    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        role="EMPLOYEE",
        is_active=True
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )
    
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    if not verify_password(user.password_hash, password):
        raise HTTPException(
            status_code=400,
            detail="Wrong Password."
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive user."
        )
    
    return user


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.services.user_service import create_user, authenticate_user
from app.services.jwt import create_access_token
from app.schemas.user import UserResponse, UserCreate
from app.schemas.auth import LoginRequest
from app.core.security import get_current_user
from app.core.permissions import require_roles
from app.core.role import Role


router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

# @router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     return create_user(db, user)


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    
    user = authenticate_user(db, req.email, req.password)
    if not user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    token = create_access_token(
        {
            "sub": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user

#test endpoint
@router.get("/admin")
def admin_test(
    current_user: User = Depends(
        require_roles(Role.ADMIN)
    ),
):
    return {"message": "Welcome Admin"}
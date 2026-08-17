from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import UserResponse
from app.crud import user as user_crud
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return user_crud.get_users(db, skip=skip, limit=limit)

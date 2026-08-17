from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import PostCreate, PostResponse, PostUpdate
from app.crud import post as post_crud
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[PostResponse])
def get_posts(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return post_crud.get_posts(db, skip=skip, limit=limit)

@router.post("/", response_model=PostResponse)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return post_crud.create_post(db, post, current_user.id)

@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    post = post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    post = post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return post_crud.update_post(db, post_id, post_update)

@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    post = post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    post_crud.delete_post(db, post_id)
    return {"message": "Post deleted"}

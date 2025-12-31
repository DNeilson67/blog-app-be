from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.database.models import User, Post
from src.database.schemas import UserResponse, PostResponse, UserUpdate
from src.middleware.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get the current user's profile
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        profile_picture=current_user.profile_picture,
        created_at=current_user.created_at
    )


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the current user's profile
    
    - **name**: New name (optional)
    - **profile_picture**: New profile picture URL (optional)
    """
    if user_data.name is not None:
        current_user.name = user_data.name
    if user_data.profile_picture is not None:
        current_user.profile_picture = user_data.profile_picture
    
    db.commit()
    db.refresh(current_user)
    
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        profile_picture=current_user.profile_picture,
        created_at=current_user.created_at
    )


@router.get("/me/posts", response_model=List[PostResponse])
async def get_user_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all posts created by the current user
    """
    posts = db.query(Post).filter(Post.author_id == current_user.id).order_by(Post.created_at.desc()).all()
    
    return [
        PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            excerpt=post.excerpt,
            category=post.category,
            author_id=post.author_id,
            author_name=current_user.name,
            created_at=post.created_at,
            updated_at=post.updated_at
        )
        for post in posts
    ]

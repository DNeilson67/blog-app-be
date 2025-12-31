from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.database.models import User, Post, Comment
from src.database.schemas import CommentCreate, CommentUpdate, CommentResponse, MessageResponse
from src.middleware.dependencies import get_current_user
import uuid
from datetime import datetime

router = APIRouter(tags=["Comments"])


@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: str,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a comment to a post
    
    - **post_id**: The ID of the post to comment on
    - **content**: Comment content (required)
    """
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    comment_id = str(uuid.uuid4())
    
    new_comment = Comment(
        id=comment_id,
        content=comment_data.content,
        post_id=post_id,
        author_id=current_user.id
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return CommentResponse(
        id=new_comment.id,
        content=new_comment.content,
        post_id=new_comment.post_id,
        author_id=new_comment.author_id,
        author_name=current_user.name,
        author_profile_picture=current_user.profile_picture,
        created_at=new_comment.created_at,
        updated_at=new_comment.updated_at
    )


@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
async def get_comments_by_post(post_id: str, db: Session = Depends(get_db)):
    """
    Get all comments for a specific post
    
    - **post_id**: The ID of the post
    """
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).all()
    
    return [
        CommentResponse(
            id=comment.id,
            content=comment.content,
            post_id=comment.post_id,
            author_id=comment.author_id,
            author_name=comment.author.name,
            author_profile_picture=comment.author.profile_picture,
            created_at=comment.created_at,
            updated_at=comment.updated_at
        )
        for comment in comments
    ]


@router.put("/comments/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: str,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Edit a comment (only the author can edit)
    
    - **comment_id**: The ID of the comment to update
    - **content**: New comment content
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Check if user is the author
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized access - only the author can edit this comment"
        )
    
    comment.content = comment_data.content
    comment.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(comment)
    
    return CommentResponse(
        id=comment.id,
        content=comment.content,
        post_id=comment.post_id,
        author_id=comment.author_id,
        author_name=comment.author.name,
        author_profile_picture=comment.author.profile_picture,
        created_at=comment.created_at,
        updated_at=comment.updated_at
    )


@router.delete("/comments/{comment_id}", response_model=MessageResponse)
async def delete_comment(
    comment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a comment (only the author can delete)
    
    - **comment_id**: The ID of the comment to delete
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Check if user is the author
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized access - only the author can delete this comment"
        )
    
    db.delete(comment)
    db.commit()
    
    return MessageResponse(message="Comment successfully deleted")

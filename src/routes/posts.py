from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.database.models import User, Post
from src.database.schemas import PostCreate, PostUpdate, PostResponse, MessageResponse
from src.middleware.dependencies import get_current_user
import uuid
from datetime import datetime

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new blog post
    
    - **title**: Post title (required)
    - **content**: Post content (required)
    - **excerpt**: Short excerpt or summary (optional)
    - **category**: Post category (optional)
    """
    post_id = str(uuid.uuid4())
    
    new_post = Post(
        id=post_id,
        title=post_data.title,
        content=post_data.content,
        excerpt=post_data.excerpt,
        category=post_data.category,
        author_id=current_user.id
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return PostResponse(
        id=new_post.id,
        title=new_post.title,
        content=new_post.content,
        excerpt=new_post.excerpt,
        category=new_post.category,
        author_id=new_post.author_id,
        author_name=current_user.name,
        created_at=new_post.created_at,
        updated_at=new_post.updated_at
    )


@router.get("", response_model=List[PostResponse])
async def get_all_posts(db: Session = Depends(get_db)):
    """
    Retrieve all blog posts
    
    Returns a list of all posts ordered by creation date (newest first)
    """
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    
    return [
        PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            excerpt=post.excerpt,
            category=post.category,
            author_id=post.author_id,
            author_name=post.author.name,
            created_at=post.created_at,
            updated_at=post.updated_at
        )
        for post in posts
    ]


@router.get("/{post_id}", response_model=PostResponse)
async def get_post_by_id(post_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific post by ID
    
    - **post_id**: The ID of the post to retrieve
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        excerpt=post.excerpt,
        category=post.category,
        author_id=post.author_id,
        author_name=post.author.name,
        created_at=post.created_at,
        updated_at=post.updated_at
    )


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Edit an existing post (only the author can edit)
    
    - **post_id**: The ID of the post to update
    - **title**: New title (optional)
    - **content**: New content (optional)
    - **excerpt**: New excerpt (optional)
    - **category**: New category (optional)
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Check if user is the author
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized access - only the author can edit this post"
        )
    
    # Update fields
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content
    if post_data.excerpt is not None:
        post.excerpt = post_data.excerpt
    if post_data.category is not None:
        post.category = post_data.category
    
    post.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(post)
    
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        excerpt=post.excerpt,
        category=post.category,
        author_id=post.author_id,
        author_name=post.author.name,
        created_at=post.created_at,
        updated_at=post.updated_at
    )


@router.delete("/{post_id}", response_model=MessageResponse)
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a post (only the author can delete)
    
    - **post_id**: The ID of the post to delete
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Check if user is the author
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized access - only the author can delete this post"
        )
    
    db.delete(post)
    db.commit()
    
    return MessageResponse(message="Post successfully deleted")

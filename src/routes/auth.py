from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.database.models import User
from src.database.schemas import UserCreate, UserLogin, Token, UserResponse, MessageResponse
from src.middleware.auth import verify_password, get_password_hash, create_access_token
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - **email**: Valid email address
    - **password**: Password (minimum 6 characters)
    - **name**: User's full name
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        id=user_id,
        email=user_data.email,
        password=hashed_password,
        name=user_data.name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": new_user.id})
    
    user_response = UserResponse(
        id=new_user.id,
        email=new_user.email,
        name=new_user.name,
        profile_picture=new_user.profile_picture,
        created_at=new_user.created_at
    )
    
    return Token(access_token=access_token, user=user_response)


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password
    
    - **email**: User's email address
    - **password**: User's password
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        profile_picture=user.profile_picture,
        created_at=user.created_at
    )
    
    return Token(access_token=access_token, user=user_response)


@router.post("/logout", response_model=MessageResponse)
async def logout():
    """
    Logout (token invalidation handled on client side)
    """
    return MessageResponse(message="Successfully logged out")

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import timedelta
import re
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from ..models.user import User, UserCreate, UserRead, UserSignIn
from ..core.database import get_session
from ..core.security import get_password_hash, create_access_token, verify_access_token
from ..core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user account.
    """
    # Validate email format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Check if username or email already exists
    existing_user_by_username = session.exec(select(User).where(User.username == user_create.username)).first()
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )

    existing_user_by_email = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create the new user
    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.post("/signin")
def signin(user_signin: UserSignIn, session: Session = Depends(get_session)):
    """
    Authenticate a user and return an access token.
    """
    username = user_signin.username
    password = user_signin.password

    # Find the user by username or email
    statement = select(User).where((User.username == username) | (User.email == username))
    user = session.exec(statement).first()

    if not user or not user.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id), "user_id": user.id, "username": user.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)) -> User:
    """
    Get the current user based on the provided JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    # Get user from database
    user = session.exec(select(User).where(User.id == int(user_id))).first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/me", response_model=UserRead)
def get_current_user_profile(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current user's profile based on the provided JWT token.
    """
    return current_user
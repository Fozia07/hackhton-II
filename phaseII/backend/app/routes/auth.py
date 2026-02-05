from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Annotated
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime
import re
import logging
from fastapi.security import OAuth2PasswordBearer

from ..models.user import User, UserCreate, UserRead, UserSignIn
from ..core.database import get_session
from ..core.security import get_password_hash, verify_password, create_access_token, verify_access_token
from ..core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(
    user_create: UserCreate = Body(...),  # ← this line is critical
    session: AsyncSession = Depends(get_session)
):
    """
    Register a new user account.
    """
    try:
        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )

        import logging
        logger = logging.getLogger(__name__)

        # Check if username or email already exists
        logger.debug("Checking for existing username")
        result_username = await session.exec(select(User).where(User.username == user_create.username))
        existing_user_by_username = result_username.first()
        if existing_user_by_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already registered"
            )

        logger.debug("Checking for existing email")
        result_email = await session.exec(select(User).where(User.email == user_create.email))
        existing_user_by_email = result_email.first()
        if existing_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        hashed_password = get_password_hash(user_create.password)

        logger.debug("Creating user object")
        # Create the new user object - explicitly set datetime fields to avoid default_factory issues
        current_time = datetime.utcnow()
        user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            created_at=current_time,
            updated_at=current_time,
            is_active=True
        )

        logger.debug("Adding user to session")
        session.add(user)

        logger.debug("Committing session")
        try:
            await session.commit()
        except Exception as db_error:
            logger.error(f"Database commit error: {str(db_error)}", exc_info=True)
            await session.rollback()
            raise

        logger.debug("Refreshing user")
        await session.refresh(user)
        logger.debug("Returning user")

        return user
    except HTTPException:
        # Re-raise HTTP exceptions as they are already properly formatted
        raise
    except Exception as e:
        # Catch any other unexpected errors and return a 500 with safe error message
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error during user signup: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration"
        )


@router.post("/signin")
async def signin(user_signin: UserSignIn, session: AsyncSession = Depends(get_session)):
    """
    Authenticate a user and return an access token.
    """
    username = user_signin.username
    password = user_signin.password

    # Find the user by username or email
    statement = select(User).where((User.username == username) | (User.email == username))
    result = await session.exec(statement)
    user = result.first()

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


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(get_session)) -> User:
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
    result = await session.exec(select(User).where(User.id == int(user_id)))
    user = result.first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/me", response_model=UserRead)
async def get_current_user_profile(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current user's profile based on the provided JWT token.
    """
    return current_user
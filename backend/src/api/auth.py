# backend/src/api/auth.py
from fastapi.security import OAuth2PasswordRequestForm
from backend.src.core.security import verify_password, create_access_token
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.db.session import get_db
from backend.src.schemas.token import Token
from backend.src.schemas.user import UserCreate, UserShow
from backend.src.models.user import User 
from backend.src.core.security import get_password_hash

router = APIRouter()

@router.post("/register", response_model=UserShow)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Check if user already exists
    # (We are skipping this check for brevity in this specific challenge)

    # 2. Hash the password
    hashed_pw = get_password_hash(user.password)

    # 3. Create the DB Model instance
    new_user = User(
        email=user.email, 
        hashed_password=hashed_pw
    )

    # 4. Add to the DB session
    db.add(new_user) #-> db.add() is synchronous, doesn't need await
    
    await db.commit() 
    await db.refresh(new_user)
    
    return new_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    #1. Fetch user by email
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    #2. Authenticate
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    #3. Create Token
    access_token_jwt = create_access_token(data={"sub": user.email})
    generated_token=Token(
        access_token=access_token_jwt,
        token_type="Bearer"
    )

    return generated_token
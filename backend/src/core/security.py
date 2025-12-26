# backend/src/security.py
from datetime import datetime, timedelta
from typing import Optional, Any, Union
from jose import jwt
from passlib.context import CryptContext

# --------------------------------------------------------------------------
# CONFIGURATION (Usually loaded from env vars, hardcoded for Phase 1)
# --------------------------------------------------------------------------
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
SECRET_KEY = "supersecretkey_change_this_in_production"

# Setup password hashing (bcrypt is the standard)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a raw password against the stored hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generates a secure hash from a raw password.
    """
    return pwd_context.hash(password)

def create_access_token(data: Optional[dict] = None, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT (JSON Web Token) for a user.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    if data is None:
        to_encode={}
    else:
        to_encode=data.copy()

    # The payload is the actual data stored inside the token
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
"""
Password Hashing and Verification Utilities.

This module provides functions for hashing new passwords and verifying existing
passwords against their stored hashes using the Passlib library.
"""
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

# Initialize the CryptContext with bcrypt as the hashing scheme.
# "deprecated="auto"" allows Passlib to handle deprecated schemes automatically.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
Global instance of CryptContext, configured for bcrypt hashing.
This context is used for all password hashing and verification operations.
"""

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a stored hashed password.

    Args:
        plain_password: The plain text password to verify.
        hashed_password: The stored hashed password to verify against.

    Returns:
        True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain text password.

    Args:
        password: The plain text password to hash.

    Returns:
        The hashed version of the password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access"):
    from jose import JWTError
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type", "access") != token_type:
            raise JWTError(f"Invalid token type: expected {token_type}")
        return payload
    except JWTError as e:
        raise e

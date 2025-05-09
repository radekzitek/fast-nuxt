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

SECRET_KEY = getattr(settings, "SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


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

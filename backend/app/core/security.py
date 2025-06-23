from datetime import datetime, timedelta
from typing import Any, Union
import hashlib
import secrets
from jose import jwt
from app.core.config import settings

ALGORITHM = "HS256"

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash using PBKDF2."""
    try:
        # Extract salt and hash from stored password
        stored_salt, stored_hash = hashed_password.split('$')
        # Hash the provided password with the same salt
        computed_hash = hashlib.pbkdf2_hmac('sha256', 
                                          plain_password.encode('utf-8'), 
                                          stored_salt.encode('utf-8'), 
                                          100000)
        return secrets.compare_digest(stored_hash.encode('utf-8'), 
                                    computed_hash.hex().encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Hash a password using PBKDF2."""
    # Generate a random salt
    salt = secrets.token_hex(32)
    # Hash the password with the salt
    password_hash = hashlib.pbkdf2_hmac('sha256', 
                                       password.encode('utf-8'), 
                                       salt.encode('utf-8'), 
                                       100000)
    # Return salt and hash separated by $
    return f"{salt}${password_hash.hex()}" 
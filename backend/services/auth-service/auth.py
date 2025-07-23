"""
Authentication utilities for Auth Service (AI SchoolOS)
"""

import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
import uuid

from models import User, Session as UserSession, Role, Permission
from schemas import UserResponse

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def hash_token(token: str) -> str:
    """Hash a token for storage."""
    return hashlib.sha256(token.encode()).hexdigest()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user with email and password."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id) -> Optional[User]:
    """Get user by ID."""
    # Always convert to string for lookup
    user_id_str = str(user_id)
    try:
        uuid.UUID(user_id_str)
    except (ValueError, TypeError):
        return None
    return db.query(User).filter(User.id == user_id_str).first()


def create_user_session(db: Session, user_id, refresh_token: str) -> UserSession:
    """Create a new user session."""
    token_hash = hash_token(refresh_token)
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    user_id_str = str(user_id)
    try:
        uuid.UUID(user_id_str)
    except (ValueError, TypeError):
        pass
    session = UserSession(
        user_id=user_id_str,
        token_hash=token_hash,
        expires_at=expires_at
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def invalidate_session(db: Session, refresh_token: str) -> bool:
    """Invalidate a user session."""
    token_hash = hash_token(refresh_token)
    session = db.query(UserSession).filter(
        UserSession.token_hash == token_hash,
        UserSession.expires_at > datetime.utcnow()
    ).first()
    
    if session:
        db.delete(session)
        db.commit()
        return True
    return False


def is_session_valid(db: Session, refresh_token: str) -> bool:
    """Check if a session is valid."""
    token_hash = hash_token(refresh_token)
    session = db.query(UserSession).filter(
        UserSession.token_hash == token_hash,
        UserSession.expires_at > datetime.utcnow()
    ).first()
    return session is not None


def get_user_permissions(db: Session, user_id) -> list:
    user_id_str = str(user_id)
    user = db.query(User).filter(User.id == user_id_str).first()
    if not user or not user.role:
        return []
    permissions = []
    for permission in user.role.permissions:
        permissions.append(f"{permission.resource}:{permission.action}")
    return permissions


def update_last_login(db: Session, user_id):
    user_id_str = str(user_id)
    user = db.query(User).filter(User.id == user_id_str).first()
    if user:
        user.last_login = datetime.utcnow()
        db.commit()


def cleanup_expired_sessions(db: Session):
    """Clean up expired sessions."""
    expired_sessions = db.query(UserSession).filter(
        UserSession.expires_at <= datetime.utcnow()
    ).all()
    
    for session in expired_sessions:
        db.delete(session)
    
    db.commit() 
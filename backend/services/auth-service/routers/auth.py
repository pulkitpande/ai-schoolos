"""
Authentication router for Auth Service (AI SchoolOS)
"""

import logging
from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from database import get_db
from auth import (
    authenticate_user, get_user_by_email, get_user_by_id, get_password_hash,
    create_access_token, create_refresh_token, verify_token, create_user_session,
    invalidate_session, is_session_valid, get_user_permissions, update_last_login
)
from dependencies import get_current_user, require_permission
from models import User, Tenant, Role, Permission
from schemas import (
    LoginRequest, LoginResponse, RegisterRequest, RegisterResponse,
    RefreshTokenRequest, RefreshTokenResponse, LogoutRequest, LogoutResponse,
    ForgotPasswordRequest, ForgotPasswordResponse, CurrentUserResponse,
    UserResponse, HealthResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.get("/")
async def root():
    return {"message": "Auth Service is running"}


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
    request: Request = None
):
    """User login endpoint."""
    try:
        # Authenticate user
        user = authenticate_user(db, login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive"
            )
        
        # Update last login
        update_last_login(db, str(user.id))
        
        # Create tokens
        access_token = create_access_token(data={"sub": str(user.id), "tenant_id": str(user.tenant_id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id), "tenant_id": str(user.tenant_id)})
        
        # Create session
        create_user_session(db, str(user.id), refresh_token)
        
        # Log successful login
        logger.info(f"User {user.email} logged in successfully from {request.client.host if request else 'unknown'}")
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60,  # 30 minutes
            user=UserResponse.from_orm(user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/register", response_model=RegisterResponse)
async def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """User registration endpoint."""
    try:
        # Check if user already exists
        existing_user = get_user_by_email(db, register_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Check if tenant exists
        tenant = db.query(Tenant).filter(Tenant.id == register_data.tenant_id).first()
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid tenant ID"
            )
        
        # Get or create default role if role_id not provided
        role_id = register_data.role_id
        if not role_id:
            # Get default role for tenant
            default_role = db.query(Role).filter(
                Role.tenant_id == register_data.tenant_id,
                Role.name == "user"
            ).first()
            
            if not default_role:
                # Create default user role
                default_role = Role(
                    name="user",
                    tenant_id=register_data.tenant_id
                )
                db.add(default_role)
                db.commit()
                db.refresh(default_role)
            
            role_id = default_role.id
        else:
            # Check if provided role exists
            role = db.query(Role).filter(Role.id == role_id).first()
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid role ID"
                )
        
        # Create new user
        hashed_password = get_password_hash(register_data.password)
        user = User(
            email=register_data.email,
            password_hash=hashed_password,
            tenant_id=register_data.tenant_id,
            role_id=role_id,
            profile_data=register_data.profile_data or {}
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create tokens
        access_token = create_access_token(data={"sub": str(user.id), "tenant_id": str(user.tenant_id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id), "tenant_id": str(user.tenant_id)})
        
        # Create session
        create_user_session(db, str(user.id), refresh_token)
        
        logger.info(f"New user registered: {user.email}")
        
        return RegisterResponse(
            user=UserResponse.from_orm(user),
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60  # 30 minutes
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token endpoint."""
    try:
        # Verify refresh token
        payload = verify_token(refresh_data.refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Check if session is valid
        if not is_session_valid(db, refresh_data.refresh_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session"
            )
        
        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")
        
        # Get user
        user = get_user_by_id(db, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new access token
        access_token = create_access_token(data={"sub": str(user.id), "tenant_id": str(user.tenant_id)})
        
        return RefreshTokenResponse(
            access_token=access_token,
            expires_in=30 * 60  # 30 minutes
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    logout_data: LogoutRequest,
    db: Session = Depends(get_db)
):
    """User logout endpoint."""
    try:
        # Invalidate session
        success = invalidate_session(db, logout_data.refresh_token)
        
        if success:
            logger.info("User logged out successfully")
            return LogoutResponse()
        else:
            # Even if session wasn't found, return success
            return LogoutResponse()
            
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/me", response_model=CurrentUserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile."""
    try:
        # Get user permissions
        permissions = get_user_permissions(db, str(current_user.id))
        
        # Get tenant
        tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
        
        # Get role (if exists)
        role = None
        if current_user.role_id:
            role = db.query(Role).filter(Role.id == current_user.role_id).first()
        
        return CurrentUserResponse(
            user=UserResponse.from_orm(current_user),
            permissions=permissions,
            role=role,
            tenant=tenant
        )
        
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(
    forgot_data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """Forgot password endpoint."""
    try:
        # Check if user exists
        user = get_user_by_email(db, forgot_data.email)
        if not user:
            # Don't reveal if user exists or not
            logger.info(f"Password reset requested for email: {forgot_data.email}")
            return ForgotPasswordResponse()
        
        # TODO: Implement password reset email sending
        # For now, just log the request
        logger.info(f"Password reset requested for user: {user.email}")
        
        return ForgotPasswordResponse()
        
    except Exception as e:
        logger.error(f"Forgot password error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/permissions", response_model=List[str])
async def get_user_permissions_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user permissions endpoint."""
    try:
        permissions = get_user_permissions(db, str(current_user.id))
        return permissions
        
    except Exception as e:
        logger.error(f"Get permissions error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 
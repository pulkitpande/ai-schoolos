"""
Unit tests for Auth Service (AI SchoolOS)
"""

import pytest
import uuid
import os
from datetime import datetime, timedelta
from auth import create_access_token, create_refresh_token


class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "auth-service"
        assert data["version"] == "1.0.0"


class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_login_success(self, client, test_user):
        """Test successful login."""
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 1800  # 30 minutes
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_register_success(self, client, test_tenant):
        """Test successful user registration."""
        register_data = {
            "email": "newuser@example.com",
            "password": "NewPassword123!",
            "tenant_id": str(test_tenant.id),
            "profile_data": {"name": "New User"}
        }
        response = client.post("/auth/register", json=register_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == "newuser@example.com"
    
    def test_register_existing_user(self, client, test_user, test_tenant):
        """Test registration with existing email."""
        register_data = {
            "email": "test@example.com",
            "password": "NewPassword123!",
            "tenant_id": str(test_tenant.id)
        }
        response = client.post("/auth/register", json=register_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    def test_register_invalid_tenant(self, client):
        """Test registration with invalid tenant ID."""
        register_data = {
            "email": "newuser@example.com",
            "password": "NewPassword123!",
            "tenant_id": str(uuid.uuid4())
        }
        response = client.post("/auth/register", json=register_data)
        assert response.status_code == 400
        assert "Invalid tenant ID" in response.json()["detail"]


class TestTokenManagement:
    """Test token management endpoints."""
    
    def test_refresh_token_success(self, client, test_user):
        """Test successful token refresh."""
        # First login to get tokens
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = client.post("/auth/login", json=login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh token
        refresh_data = {"refresh_token": refresh_token}
        response = client.post("/auth/refresh", json=refresh_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_refresh_token_invalid(self, client):
        """Test token refresh with invalid token."""
        refresh_data = {"refresh_token": "invalid_token"}
        response = client.post("/auth/refresh", json=refresh_data)
        assert response.status_code == 401
        assert "Invalid refresh token" in response.json()["detail"]
    
    def test_logout_success(self, client, test_user):
        """Test successful logout."""
        # First login to get tokens
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = client.post("/auth/login", json=login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        # Logout
        logout_data = {"refresh_token": refresh_token}
        response = client.post("/auth/logout", json=logout_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully logged out"


class TestUserProfile:
    """Test user profile endpoints."""
    
    def test_get_current_user(self, client, test_user):
        """Test getting current user profile."""
        # First login to get access token
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = client.post("/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]
        
        # Get current user
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == "test@example.com"
        assert "permissions" in data
        assert "tenant" in data
    
    def test_get_current_user_no_token(self, client):
        """Test getting current user without token."""
        response = client.get("/auth/me")
        assert response.status_code == 403  # FastAPI security returns 403 for missing token
    
    def test_get_permissions(self, client, test_user):
        """Test getting user permissions."""
        # First login to get access token
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = client.post("/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]
        
        # Get permissions
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/auth/permissions", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestPasswordReset:
    """Test password reset endpoints."""
    
    def test_forgot_password(self, client, test_user):
        """Test forgot password endpoint."""
        forgot_data = {"email": "test@example.com"}
        response = client.post("/auth/forgot-password", json=forgot_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Password reset email sent successfully"
    
    def test_forgot_password_nonexistent_user(self, client):
        """Test forgot password with nonexistent user."""
        forgot_data = {"email": "nonexistent@example.com"}
        response = client.post("/auth/forgot-password", json=forgot_data)
        assert response.status_code == 200  # Should not reveal if user exists
        assert response.json()["message"] == "Password reset email sent successfully"


class TestValidation:
    """Test input validation."""
    
    def test_register_weak_password(self, client, test_tenant):
        """Test registration with weak password."""
        register_data = {
            "email": "newuser@example.com",
            "password": "weak",
            "tenant_id": str(test_tenant.id)
        }
        response = client.post("/auth/register", json=register_data)
        assert response.status_code == 422  # Validation error
    
    def test_register_invalid_email(self, client, test_tenant):
        """Test registration with invalid email."""
        register_data = {
            "email": "invalid-email",
            "password": "ValidPassword123!",
            "tenant_id": str(test_tenant.id)
        }
        response = client.post("/auth/register", json=register_data)
        assert response.status_code == 422  # Validation error 
"""
Test configuration and fixtures for Auth Service
"""

import sys
import os
# NOTE: This sys.path hack is for test discovery only. It does NOT affect production or deployed code.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from main import app
from database import get_db
from models import Base, User, Tenant, Role, Permission
from auth import get_password_hash


@pytest.fixture(scope="function")
def db_engine():
    """Create a unique in-memory database for each test."""
    # Create unique database URL for each test
    unique_db_url = f"sqlite:///file:test_{uuid.uuid4().hex}?mode=memory&cache=shared"
    engine = create_engine(
        unique_db_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Clean up
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a test database session with isolated database."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db_engine):
    """Create a test client with isolated database."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    
    def override_get_db():
        """Override database dependency for testing."""
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    client = TestClient(app)
    yield client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def test_tenant(db_session):
    """Create a test tenant."""
    tenant = Tenant(
        id=uuid.uuid4(),
        name="Test School",
        domain="test.school.com",
        config={},
        subscription_tier="basic",
        is_active=True
    )
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)
    return tenant


@pytest.fixture
def test_role(db_session, test_tenant):
    """Create a test role."""
    role = Role(
        id=uuid.uuid4(),
        name="admin",
        tenant_id=test_tenant.id
    )
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)
    return role


@pytest.fixture
def test_user(db_session, test_tenant, test_role):
    """Create a test user."""
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        password_hash=get_password_hash("TestPassword123!"),
        tenant_id=test_tenant.id,
        role_id=test_role.id,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user 
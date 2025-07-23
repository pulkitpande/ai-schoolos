"""
Test Configuration and Fixtures (AI SchoolOS)

Comprehensive test setup with database fixtures, authentication mocks, and service communication testing
"""

import pytest
import asyncio
from typing import Generator, Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import tempfile
import os
import json
from datetime import datetime, timedelta
from jose import jwt

# Test database URL
TEST_DATABASE_URL = "sqlite:///:memory:"

# Test JWT settings
TEST_SECRET_KEY = "test-secret-key"
TEST_ALGORITHM = "HS256"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create test database session."""
    # Create tables
    from shared.database.models import Base
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop tables
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def test_client():
    """Create test client."""
    from fastapi.testclient import TestClient
    from main import app
    
    with TestClient(app) as client:
        yield client


@pytest.fixture
def auth_headers():
    """Create authentication headers for testing."""
    def _create_auth_headers(user_id: str = "test-user-id", roles: list = None, permissions: list = None):
        payload = {
            "sub": user_id,
            "email": "test@example.com",
            "roles": roles or ["user"],
            "permissions": permissions or ["read"],
            "tenant_id": "test-tenant-id",
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        
        token = jwt.encode(payload, TEST_SECRET_KEY, algorithm=TEST_ALGORITHM)
        return {"Authorization": f"Bearer {token}"}
    
    return _create_auth_headers


@pytest.fixture
def service_headers():
    """Create service-to-service authentication headers."""
    def _create_service_headers(service_name: str = "test-service", permissions: list = None):
        payload = {
            "service": service_name,
            "permissions": permissions or ["read"],
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        
        token = jwt.encode(payload, TEST_SECRET_KEY, algorithm=TEST_ALGORITHM)
        return {
            "X-Service-Token": token,
            "X-Service-Name": service_name,
            "Content-Type": "application/json"
        }
    
    return _create_service_headers


@pytest.fixture
def mock_user():
    """Create mock user data."""
    return {
        "id": "test-user-id",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "roles": ["user"],
        "permissions": ["read"],
        "tenant_id": "test-tenant-id",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@pytest.fixture
def mock_tenant():
    """Create mock tenant data."""
    return {
        "id": "test-tenant-id",
        "name": "Test School",
        "domain": "test.example.com",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@pytest.fixture
def mock_student():
    """Create mock student data."""
    return {
        "id": "test-student-id",
        "tenant_id": "test-tenant-id",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "date_of_birth": "2010-01-01",
        "gender": "male",
        "address": "123 Test St",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@pytest.fixture
def mock_teacher():
    """Create mock teacher data."""
    return {
        "id": "test-teacher-id",
        "tenant_id": "test-tenant-id",
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone": "+1234567891",
        "subject": "Mathematics",
        "qualification": "M.Sc. Mathematics",
        "experience_years": 5,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@pytest.fixture
def mock_attendance_record():
    """Create mock attendance record data."""
    return {
        "id": "test-attendance-id",
        "tenant_id": "test-tenant-id",
        "student_id": "test-student-id",
        "class_id": "test-class-id",
        "section_id": "test-section-id",
        "attendance_date": datetime.now().date(),
        "attendance_status": "present",
        "attendance_type": "manual",
        "check_in_time": datetime.utcnow(),
        "check_out_time": None,
        "late_minutes": 0,
        "remarks": "Test attendance",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@pytest.fixture
def mock_timetable_slot():
    """Create mock timetable slot data."""
    return {
        "id": "test-slot-id",
        "tenant_id": "test-tenant-id",
        "class_id": "test-class-id",
        "section_id": "test-section-id",
        "subject_id": "test-subject-id",
        "teacher_id": "test-teacher-id",
        "room_id": "test-room-id",
        "time_slot_id": "test-time-slot-id",
        "day_of_week": "monday",
        "start_time": datetime.strptime("09:00", "%H:%M").time(),
        "end_time": datetime.strptime("10:00", "%H:%M").time(),
        "academic_year": "2024-25",
        "semester": "first",
        "is_active": True,
        "is_recurring": True,
        "created_by": "test-user-id",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@pytest.fixture
def mock_transport_booking():
    """Create mock transport booking data."""
    return {
        "id": "test-booking-id",
        "tenant_id": "test-tenant-id",
        "student_id": "test-student-id",
        "schedule_id": "test-schedule-id",
        "pickup_stop_id": "test-pickup-stop-id",
        "drop_stop_id": "test-drop-stop-id",
        "booking_date": datetime.now().date(),
        "booking_type": "daily",
        "fare_amount": 50.0,
        "booking_status": "confirmed",
        "payment_status": "paid",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@pytest.fixture
def mock_notification():
    """Create mock notification data."""
    return {
        "id": "test-notification-id",
        "tenant_id": "test-tenant-id",
        "title": "Test Notification",
        "message": "This is a test notification",
        "notification_type": "info",
        "recipient_type": "student",
        "recipient_id": "test-student-id",
        "channel": "email",
        "status": "sent",
        "sent_at": datetime.utcnow(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@pytest.fixture
def mock_analytics_data():
    """Create mock analytics data."""
    return {
        "id": "test-analytics-id",
        "tenant_id": "test-tenant-id",
        "data_type": "attendance",
        "data_period": "daily",
        "data_date": datetime.now().date(),
        "metrics": {
            "total_students": 100,
            "present_count": 85,
            "absent_count": 10,
            "late_count": 5,
            "attendance_rate": 85.0
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@pytest.fixture
def mock_service_response():
    """Create mock service response."""
    return {
        "success": True,
        "data": {
            "id": "test-id",
            "name": "Test Data",
            "created_at": datetime.utcnow().isoformat()
        },
        "message": "Success"
    }


@pytest.fixture
def mock_error_response():
    """Create mock error response."""
    return {
        "success": False,
        "error": "Test error message",
        "details": "Additional error details"
    }


@pytest.fixture
def test_config():
    """Create test configuration."""
    return {
        "database_url": TEST_DATABASE_URL,
        "secret_key": TEST_SECRET_KEY,
        "algorithm": TEST_ALGORITHM,
        "access_token_expire_minutes": 30,
        "refresh_token_expire_days": 7,
        "service_name": "test-service",
        "tenant_id": "test-tenant-id"
    }


@pytest.fixture
def mock_metrics():
    """Create mock metrics data."""
    return {
        "request_count": 100,
        "request_duration": 1.5,
        "active_connections": 10,
        "memory_usage": 1024 * 1024 * 100,  # 100MB
        "cpu_usage": 25.5,
        "error_count": 2
    }


@pytest.fixture
def mock_health_check():
    """Create mock health check response."""
    return {
        "status": "healthy",
        "service": "test-service",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "database": {"status": "healthy", "message": "Database connection OK"},
            "system": {
                "status": "healthy",
                "memory_usage": 45.2,
                "cpu_usage": 12.5,
                "disk_usage": 65.8
            }
        }
    }


class MockServiceClient:
    """Mock service client for testing."""
    
    def __init__(self, responses: Dict[str, Any] = None):
        self.responses = responses or {}
        self.calls = []
    
    async def get(self, service_name: str, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Mock GET request."""
        key = f"{service_name}:GET:{endpoint}"
        self.calls.append({
            "method": "GET",
            "service": service_name,
            "endpoint": endpoint,
            "params": params
        })
        return self.responses.get(key, {"success": True, "data": {}})
    
    async def post(self, service_name: str, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock POST request."""
        key = f"{service_name}:POST:{endpoint}"
        self.calls.append({
            "method": "POST",
            "service": service_name,
            "endpoint": endpoint,
            "data": data
        })
        return self.responses.get(key, {"success": True, "data": {}})
    
    async def put(self, service_name: str, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock PUT request."""
        key = f"{service_name}:PUT:{endpoint}"
        self.calls.append({
            "method": "PUT",
            "service": service_name,
            "endpoint": endpoint,
            "data": data
        })
        return self.responses.get(key, {"success": True, "data": {}})
    
    async def delete(self, service_name: str, endpoint: str) -> Dict[str, Any]:
        """Mock DELETE request."""
        key = f"{service_name}:DELETE:{endpoint}"
        self.calls.append({
            "method": "DELETE",
            "service": service_name,
            "endpoint": endpoint
        })
        return self.responses.get(key, {"success": True, "data": {}})


@pytest.fixture
def mock_service_client():
    """Create mock service client."""
    return MockServiceClient()


@pytest.fixture
def mock_service_client_with_responses():
    """Create mock service client with predefined responses."""
    responses = {
        "auth-service:GET:/api/v1/auth/users/test-user-id": {
            "success": True,
            "data": {
                "id": "test-user-id",
                "email": "test@example.com",
                "roles": ["user"],
                "permissions": ["read"]
            }
        },
        "student-service:GET:/api/v1/students/test-student-id": {
            "success": True,
            "data": {
                "id": "test-student-id",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com"
            }
        }
    }
    return MockServiceClient(responses)


# Test utilities
def create_test_token(user_id: str = "test-user-id", roles: list = None, permissions: list = None) -> str:
    """Create a test JWT token."""
    payload = {
        "sub": user_id,
        "email": "test@example.com",
        "roles": roles or ["user"],
        "permissions": permissions or ["read"],
        "tenant_id": "test-tenant-id",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, TEST_SECRET_KEY, algorithm=TEST_ALGORITHM)


def create_test_service_token(service_name: str = "test-service", permissions: list = None) -> str:
    """Create a test service token."""
    payload = {
        "service": service_name,
        "permissions": permissions or ["read"],
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, TEST_SECRET_KEY, algorithm=TEST_ALGORITHM)


def assert_response_structure(response_data: Dict[str, Any]):
    """Assert common response structure."""
    assert "success" in response_data
    assert isinstance(response_data["success"], bool)
    
    if response_data["success"]:
        assert "data" in response_data
    else:
        assert "error" in response_data


def assert_pagination_structure(response_data: Dict[str, Any]):
    """Assert pagination response structure."""
    assert "items" in response_data
    assert "total" in response_data
    assert "page" in response_data
    assert "size" in response_data
    assert isinstance(response_data["items"], list)
    assert isinstance(response_data["total"], int)
    assert isinstance(response_data["page"], int)
    assert isinstance(response_data["size"], int) 
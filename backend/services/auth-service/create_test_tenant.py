#!/usr/bin/env python3
"""
Script to create a test tenant for manual API testing
"""

import os
import uuid
from sqlalchemy.orm import Session

from database import SessionLocal, create_tables
from models import Tenant, Role

def create_test_tenant():
    """Create a test tenant and default roles."""
    db = SessionLocal()
    try:
        # Create tables if they don't exist
        create_tables()
        
        # Create test tenant
        tenant = Tenant(
            id=str(uuid.uuid4()),
            name="Test School",
            domain="test.school.com",
            config={},
            subscription_tier="basic",
            is_active=True
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        
        # Create default roles
        admin_role = Role(
            id=str(uuid.uuid4()),
            name="admin",
            tenant_id=tenant.id
        )
        user_role = Role(
            id=str(uuid.uuid4()),
            name="user",
            tenant_id=tenant.id
        )
        
        db.add(admin_role)
        db.add(user_role)
        db.commit()
        
        print(f"✅ Test tenant created successfully!")
        print(f"   Tenant ID: {tenant.id}")
        print(f"   Tenant Name: {tenant.name}")
        print(f"   Domain: {tenant.domain}")
        print(f"   Admin Role ID: {admin_role.id}")
        print(f"   User Role ID: {user_role.id}")
        print(f"\nYou can now use tenant_id: '{tenant.id}' for testing registration")
        
    except Exception as e:
        print(f"❌ Error creating test tenant: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_tenant() 
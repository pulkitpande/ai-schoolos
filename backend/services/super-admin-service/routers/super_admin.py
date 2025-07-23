"""
Super Admin Service Router

Handles all super admin operations including tenant management, system configuration, and administrative functions.
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..database import get_db
from ..models import (
    Tenant, SystemConfig, AdminUser, AuditLog, SystemBackup, 
    SystemMaintenance, License, Subscription
)
from ..schemas import (
    TenantCreate, TenantUpdate, TenantResponse,
    SystemConfigCreate, SystemConfigUpdate, SystemConfigResponse,
    AdminUserCreate, AdminUserUpdate, AdminUserResponse,
    AuditLogResponse, SystemBackupCreate, SystemBackupResponse,
    SystemMaintenanceCreate, SystemMaintenanceUpdate, SystemMaintenanceResponse,
    LicenseCreate, LicenseUpdate, LicenseResponse,
    SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
)

router = APIRouter(prefix="/super-admin", tags=["super-admin"])


# Tenant Management
@router.post("/tenants", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    tenant: TenantCreate,
    db: Session = Depends(get_db)
):
    """Create a new tenant."""
    try:
        db_tenant = Tenant(
            tenant_name=tenant.tenant_name,
            tenant_code=tenant.tenant_code,
            domain=tenant.domain,
            contact_person=tenant.contact_person,
            contact_email=tenant.contact_email,
            contact_phone=tenant.contact_phone,
            address=tenant.address,
            city=tenant.city,
            state=tenant.state,
            country=tenant.country,
            postal_code=tenant.postal_code,
            timezone=tenant.timezone,
            currency=tenant.currency,
            language=tenant.language,
            max_users=tenant.max_users,
            max_students=tenant.max_students,
            subscription_plan=tenant.subscription_plan,
            subscription_status=tenant.subscription_status,
            trial_end_date=tenant.trial_end_date,
            settings=tenant.settings
        )
        db.add(db_tenant)
        db.commit()
        db.refresh(db_tenant)
        return TenantResponse.from_orm(db_tenant)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tenants", response_model=List[TenantResponse])
async def get_tenants(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    subscription_status: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """Get all tenants with optional filters."""
    query = db.query(Tenant)
    
    if subscription_status:
        query = query.filter(Tenant.subscription_status == subscription_status)
    if is_active is not None:
        query = query.filter(Tenant.is_active == is_active)
    
    tenants = query.offset(skip).limit(limit).all()
    return [TenantResponse.from_orm(tenant) for tenant in tenants]


@router.get("/tenants/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific tenant by ID."""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return TenantResponse.from_orm(tenant)


@router.put("/tenants/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: str,
    tenant: TenantUpdate,
    db: Session = Depends(get_db)
):
    """Update a tenant."""
    db_tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    for field, value in tenant.dict(exclude_unset=True).items():
        setattr(db_tenant, field, value)
    
    db_tenant.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_tenant)
    return TenantResponse.from_orm(db_tenant)


@router.delete("/tenants/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    tenant_id: str,
    db: Session = Depends(get_db)
):
    """Delete a tenant (soft delete)."""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    tenant.is_active = False
    tenant.updated_at = datetime.utcnow()
    db.commit()


# System Configuration Management
@router.post("/config", response_model=SystemConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_system_config(
    config: SystemConfigCreate,
    db: Session = Depends(get_db)
):
    """Create a new system configuration."""
    try:
        db_config = SystemConfig(
            config_key=config.config_key,
            config_value=config.config_value,
            config_type=config.config_type,
            description=config.description,
            is_encrypted=config.is_encrypted,
            is_sensitive=config.is_sensitive
        )
        db.add(db_config)
        db.commit()
        db.refresh(db_config)
        return SystemConfigResponse.from_orm(db_config)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/config", response_model=List[SystemConfigResponse])
async def get_system_configs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    config_type: Optional[str] = None
):
    """Get all system configurations with optional filters."""
    query = db.query(SystemConfig)
    
    if config_type:
        query = query.filter(SystemConfig.config_type == config_type)
    
    configs = query.offset(skip).limit(limit).all()
    return [SystemConfigResponse.from_orm(config) for config in configs]


@router.get("/config/{config_id}", response_model=SystemConfigResponse)
async def get_system_config(
    config_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific system configuration by ID."""
    config = db.query(SystemConfig).filter(SystemConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="System configuration not found")
    
    return SystemConfigResponse.from_orm(config)


@router.put("/config/{config_id}", response_model=SystemConfigResponse)
async def update_system_config(
    config_id: str,
    config: SystemConfigUpdate,
    db: Session = Depends(get_db)
):
    """Update a system configuration."""
    db_config = db.query(SystemConfig).filter(SystemConfig.id == config_id).first()
    
    if not db_config:
        raise HTTPException(status_code=404, detail="System configuration not found")
    
    for field, value in config.dict(exclude_unset=True).items():
        setattr(db_config, field, value)
    
    db_config.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_config)
    return SystemConfigResponse.from_orm(db_config)


@router.delete("/config/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system_config(
    config_id: str,
    db: Session = Depends(get_db)
):
    """Delete a system configuration."""
    config = db.query(SystemConfig).filter(SystemConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="System configuration not found")
    
    db.delete(config)
    db.commit()


# Admin User Management
@router.post("/admin-users", response_model=AdminUserResponse, status_code=status.HTTP_201_CREATED)
async def create_admin_user(
    admin_user: AdminUserCreate,
    db: Session = Depends(get_db)
):
    """Create a new admin user."""
    try:
        db_admin_user = AdminUser(
            username=admin_user.username,
            email=admin_user.email,
            full_name=admin_user.full_name,
            role=admin_user.role,
            permissions=admin_user.permissions,
            is_super_admin=admin_user.is_super_admin,
            last_login=admin_user.last_login,
            password_hash=admin_user.password_hash
        )
        db.add(db_admin_user)
        db.commit()
        db.refresh(db_admin_user)
        return AdminUserResponse.from_orm(db_admin_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/admin-users", response_model=List[AdminUserResponse])
async def get_admin_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    role: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """Get all admin users with optional filters."""
    query = db.query(AdminUser)
    
    if role:
        query = query.filter(AdminUser.role == role)
    if is_active is not None:
        query = query.filter(AdminUser.is_active == is_active)
    
    admin_users = query.offset(skip).limit(limit).all()
    return [AdminUserResponse.from_orm(admin_user) for admin_user in admin_users]


@router.get("/admin-users/{admin_user_id}", response_model=AdminUserResponse)
async def get_admin_user(
    admin_user_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific admin user by ID."""
    admin_user = db.query(AdminUser).filter(AdminUser.id == admin_user_id).first()
    
    if not admin_user:
        raise HTTPException(status_code=404, detail="Admin user not found")
    
    return AdminUserResponse.from_orm(admin_user)


@router.put("/admin-users/{admin_user_id}", response_model=AdminUserResponse)
async def update_admin_user(
    admin_user_id: str,
    admin_user: AdminUserUpdate,
    db: Session = Depends(get_db)
):
    """Update an admin user."""
    db_admin_user = db.query(AdminUser).filter(AdminUser.id == admin_user_id).first()
    
    if not db_admin_user:
        raise HTTPException(status_code=404, detail="Admin user not found")
    
    for field, value in admin_user.dict(exclude_unset=True).items():
        setattr(db_admin_user, field, value)
    
    db_admin_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_admin_user)
    return AdminUserResponse.from_orm(db_admin_user)


@router.delete("/admin-users/{admin_user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin_user(
    admin_user_id: str,
    db: Session = Depends(get_db)
):
    """Delete an admin user (soft delete)."""
    admin_user = db.query(AdminUser).filter(AdminUser.id == admin_user_id).first()
    
    if not admin_user:
        raise HTTPException(status_code=404, detail="Admin user not found")
    
    admin_user.is_active = False
    admin_user.updated_at = datetime.utcnow()
    db.commit()


# Audit Log Management
@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """Get audit logs with optional filters."""
    query = db.query(AuditLog)
    
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if action:
        query = query.filter(AuditLog.action == action)
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)
    if start_date:
        query = query.filter(AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AuditLog.timestamp <= end_date)
    
    audit_logs = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    return [AuditLogResponse.from_orm(log) for log in audit_logs]


@router.get("/audit-logs/{log_id}", response_model=AuditLogResponse)
async def get_audit_log(
    log_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific audit log by ID."""
    audit_log = db.query(AuditLog).filter(AuditLog.id == log_id).first()
    
    if not audit_log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    
    return AuditLogResponse.from_orm(audit_log)


# System Backup Management
@router.post("/backups", response_model=SystemBackupResponse, status_code=status.HTTP_201_CREATED)
async def create_system_backup(
    backup: SystemBackupCreate,
    db: Session = Depends(get_db)
):
    """Create a new system backup."""
    try:
        db_backup = SystemBackup(
            backup_name=backup.backup_name,
            backup_type=backup.backup_type,
            backup_size=backup.backup_size,
            file_path=backup.file_path,
            checksum=backup.checksum,
            compression_type=backup.compression_type,
            encryption_type=backup.encryption_type,
            backup_notes=backup.backup_notes
        )
        db.add(db_backup)
        db.commit()
        db.refresh(db_backup)
        return SystemBackupResponse.from_orm(db_backup)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/backups", response_model=List[SystemBackupResponse])
async def get_system_backups(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    backup_type: Optional[str] = None,
    status: Optional[str] = None
):
    """Get all system backups with optional filters."""
    query = db.query(SystemBackup)
    
    if backup_type:
        query = query.filter(SystemBackup.backup_type == backup_type)
    if status:
        query = query.filter(SystemBackup.status == status)
    
    backups = query.order_by(SystemBackup.created_at.desc()).offset(skip).limit(limit).all()
    return [SystemBackupResponse.from_orm(backup) for backup in backups]


@router.get("/backups/{backup_id}", response_model=SystemBackupResponse)
async def get_system_backup(
    backup_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific system backup by ID."""
    backup = db.query(SystemBackup).filter(SystemBackup.id == backup_id).first()
    
    if not backup:
        raise HTTPException(status_code=404, detail="System backup not found")
    
    return SystemBackupResponse.from_orm(backup)


@router.delete("/backups/{backup_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system_backup(
    backup_id: str,
    db: Session = Depends(get_db)
):
    """Delete a system backup."""
    backup = db.query(SystemBackup).filter(SystemBackup.id == backup_id).first()
    
    if not backup:
        raise HTTPException(status_code=404, detail="System backup not found")
    
    db.delete(backup)
    db.commit()


# System Maintenance Management
@router.post("/maintenance", response_model=SystemMaintenanceResponse, status_code=status.HTTP_201_CREATED)
async def create_system_maintenance(
    maintenance: SystemMaintenanceCreate,
    db: Session = Depends(get_db)
):
    """Create a new system maintenance record."""
    try:
        db_maintenance = SystemMaintenance(
            maintenance_type=maintenance.maintenance_type,
            title=maintenance.title,
            description=maintenance.description,
            scheduled_start=maintenance.scheduled_start,
            scheduled_end=maintenance.scheduled_end,
            affected_services=maintenance.affected_services,
            maintenance_window=maintenance.maintenance_window,
            priority=maintenance.priority,
            assigned_to=maintenance.assigned_to,
            maintenance_notes=maintenance.maintenance_notes
        )
        db.add(db_maintenance)
        db.commit()
        db.refresh(db_maintenance)
        return SystemMaintenanceResponse.from_orm(db_maintenance)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/maintenance", response_model=List[SystemMaintenanceResponse])
async def get_system_maintenance(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    maintenance_type: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None
):
    """Get all system maintenance records with optional filters."""
    query = db.query(SystemMaintenance)
    
    if maintenance_type:
        query = query.filter(SystemMaintenance.maintenance_type == maintenance_type)
    if status:
        query = query.filter(SystemMaintenance.status == status)
    if priority:
        query = query.filter(SystemMaintenance.priority == priority)
    
    maintenance_records = query.order_by(SystemMaintenance.scheduled_start.desc()).offset(skip).limit(limit).all()
    return [SystemMaintenanceResponse.from_orm(record) for record in maintenance_records]


@router.get("/maintenance/{maintenance_id}", response_model=SystemMaintenanceResponse)
async def get_system_maintenance_record(
    maintenance_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific system maintenance record by ID."""
    maintenance = db.query(SystemMaintenance).filter(SystemMaintenance.id == maintenance_id).first()
    
    if not maintenance:
        raise HTTPException(status_code=404, detail="System maintenance record not found")
    
    return SystemMaintenanceResponse.from_orm(maintenance)


@router.put("/maintenance/{maintenance_id}", response_model=SystemMaintenanceResponse)
async def update_system_maintenance(
    maintenance_id: str,
    maintenance: SystemMaintenanceUpdate,
    db: Session = Depends(get_db)
):
    """Update a system maintenance record."""
    db_maintenance = db.query(SystemMaintenance).filter(SystemMaintenance.id == maintenance_id).first()
    
    if not db_maintenance:
        raise HTTPException(status_code=404, detail="System maintenance record not found")
    
    for field, value in maintenance.dict(exclude_unset=True).items():
        setattr(db_maintenance, field, value)
    
    db_maintenance.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_maintenance)
    return SystemMaintenanceResponse.from_orm(db_maintenance)


@router.delete("/maintenance/{maintenance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system_maintenance(
    maintenance_id: str,
    db: Session = Depends(get_db)
):
    """Delete a system maintenance record."""
    maintenance = db.query(SystemMaintenance).filter(SystemMaintenance.id == maintenance_id).first()
    
    if not maintenance:
        raise HTTPException(status_code=404, detail="System maintenance record not found")
    
    db.delete(maintenance)
    db.commit()


# License Management
@router.post("/licenses", response_model=LicenseResponse, status_code=status.HTTP_201_CREATED)
async def create_license(
    license_data: LicenseCreate,
    db: Session = Depends(get_db)
):
    """Create a new license."""
    try:
        db_license = License(
            license_key=license_data.license_key,
            license_type=license_data.license_type,
            tenant_id=license_data.tenant_id,
            features=license_data.features,
            max_users=license_data.max_users,
            max_students=license_data.max_students,
            valid_from=license_data.valid_from,
            valid_until=license_data.valid_until,
            is_active=license_data.is_active,
            license_notes=license_data.license_notes
        )
        db.add(db_license)
        db.commit()
        db.refresh(db_license)
        return LicenseResponse.from_orm(db_license)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/licenses", response_model=List[LicenseResponse])
async def get_licenses(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    license_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    tenant_id: Optional[str] = None
):
    """Get all licenses with optional filters."""
    query = db.query(License)
    
    if license_type:
        query = query.filter(License.license_type == license_type)
    if is_active is not None:
        query = query.filter(License.is_active == is_active)
    if tenant_id:
        query = query.filter(License.tenant_id == tenant_id)
    
    licenses = query.offset(skip).limit(limit).all()
    return [LicenseResponse.from_orm(license) for license in licenses]


@router.get("/licenses/{license_id}", response_model=LicenseResponse)
async def get_license(
    license_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific license by ID."""
    license_record = db.query(License).filter(License.id == license_id).first()
    
    if not license_record:
        raise HTTPException(status_code=404, detail="License not found")
    
    return LicenseResponse.from_orm(license_record)


@router.put("/licenses/{license_id}", response_model=LicenseResponse)
async def update_license(
    license_id: str,
    license_data: LicenseUpdate,
    db: Session = Depends(get_db)
):
    """Update a license."""
    db_license = db.query(License).filter(License.id == license_id).first()
    
    if not db_license:
        raise HTTPException(status_code=404, detail="License not found")
    
    for field, value in license_data.dict(exclude_unset=True).items():
        setattr(db_license, field, value)
    
    db_license.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_license)
    return LicenseResponse.from_orm(db_license)


@router.delete("/licenses/{license_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_license(
    license_id: str,
    db: Session = Depends(get_db)
):
    """Delete a license."""
    license_record = db.query(License).filter(License.id == license_id).first()
    
    if not license_record:
        raise HTTPException(status_code=404, detail="License not found")
    
    db.delete(license_record)
    db.commit()


# Subscription Management
@router.post("/subscriptions", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db)
):
    """Create a new subscription."""
    try:
        db_subscription = Subscription(
            tenant_id=subscription.tenant_id,
            plan_name=subscription.plan_name,
            plan_type=subscription.plan_type,
            billing_cycle=subscription.billing_cycle,
            amount=subscription.amount,
            currency=subscription.currency,
            start_date=subscription.start_date,
            end_date=subscription.end_date,
            trial_end_date=subscription.trial_end_date,
            status=subscription.status,
            payment_method=subscription.payment_method,
            auto_renew=subscription.auto_renew,
            subscription_notes=subscription.subscription_notes
        )
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return SubscriptionResponse.from_orm(db_subscription)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/subscriptions", response_model=List[SubscriptionResponse])
async def get_subscriptions(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    plan_type: Optional[str] = None,
    status: Optional[str] = None,
    tenant_id: Optional[str] = None
):
    """Get all subscriptions with optional filters."""
    query = db.query(Subscription)
    
    if plan_type:
        query = query.filter(Subscription.plan_type == plan_type)
    if status:
        query = query.filter(Subscription.status == status)
    if tenant_id:
        query = query.filter(Subscription.tenant_id == tenant_id)
    
    subscriptions = query.offset(skip).limit(limit).all()
    return [SubscriptionResponse.from_orm(subscription) for subscription in subscriptions]


@router.get("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(
    subscription_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific subscription by ID."""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    return SubscriptionResponse.from_orm(subscription)


@router.put("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
async def update_subscription(
    subscription_id: str,
    subscription: SubscriptionUpdate,
    db: Session = Depends(get_db)
):
    """Update a subscription."""
    db_subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    for field, value in subscription.dict(exclude_unset=True).items():
        setattr(db_subscription, field, value)
    
    db_subscription.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_subscription)
    return SubscriptionResponse.from_orm(db_subscription)


@router.delete("/subscriptions/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription(
    subscription_id: str,
    db: Session = Depends(get_db)
):
    """Delete a subscription."""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(subscription)
    db.commit()


# Health Check
@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "super-admin-service",
        "timestamp": datetime.utcnow().isoformat()
    } 
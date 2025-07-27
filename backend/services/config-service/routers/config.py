"""
Config Service Router

Handles all configuration-related operations including system settings, feature flags, and configuration management.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from database import get_db
from ..models import (
    SystemConfig, FeatureFlag, EnvironmentConfig, ServiceConfig, 
    ConfigTemplate, ConfigOverride
)
from ..schemas import (
    SystemConfigCreate, SystemConfigUpdate, SystemConfigResponse,
    FeatureFlagCreate, FeatureFlagUpdate, FeatureFlagResponse,
    EnvironmentConfigCreate, EnvironmentConfigUpdate, EnvironmentConfigResponse,
    ServiceConfigCreate, ServiceConfigUpdate, ServiceConfigResponse,
    ConfigTemplateCreate, ConfigTemplateUpdate, ConfigTemplateResponse,
    ConfigOverrideCreate, ConfigOverrideUpdate, ConfigOverrideResponse
)

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/")
async def root():
    return {"message": "Config Service is running"}


# System Configuration Management
@router.post("/system", response_model=SystemConfigResponse, status_code=status.HTTP_201_CREATED)
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
            is_sensitive=config.is_sensitive,
            category=config.category,
            version=config.version
        )
        db.add(db_config)
        db.commit()
        db.refresh(db_config)
        return SystemConfigResponse.from_orm(db_config)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/system", response_model=List[SystemConfigResponse])
async def get_system_configs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    config_type: Optional[str] = None
):
    """Get all system configurations with optional filters."""
    query = db.query(SystemConfig)
    
    if category:
        query = query.filter(SystemConfig.category == category)
    if config_type:
        query = query.filter(SystemConfig.config_type == config_type)
    
    configs = query.offset(skip).limit(limit).all()
    return [SystemConfigResponse.from_orm(config) for config in configs]


@router.get("/system/{config_id}", response_model=SystemConfigResponse)
async def get_system_config(
    config_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific system configuration by ID."""
    config = db.query(SystemConfig).filter(SystemConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="System configuration not found")
    
    return SystemConfigResponse.from_orm(config)


@router.get("/system/key/{config_key}", response_model=SystemConfigResponse)
async def get_system_config_by_key(
    config_key: str,
    db: Session = Depends(get_db)
):
    """Get a system configuration by key."""
    config = db.query(SystemConfig).filter(SystemConfig.config_key == config_key).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="System configuration not found")
    
    return SystemConfigResponse.from_orm(config)


@router.put("/system/{config_id}", response_model=SystemConfigResponse)
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


@router.delete("/system/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
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


# Feature Flag Management
@router.post("/features", response_model=FeatureFlagResponse, status_code=status.HTTP_201_CREATED)
async def create_feature_flag(
    feature_flag: FeatureFlagCreate,
    db: Session = Depends(get_db)
):
    """Create a new feature flag."""
    try:
        db_feature_flag = FeatureFlag(
            flag_name=feature_flag.flag_name,
            flag_key=feature_flag.flag_key,
            description=feature_flag.description,
            is_enabled=feature_flag.is_enabled,
            rollout_percentage=feature_flag.rollout_percentage,
            target_tenants=feature_flag.target_tenants,
            target_users=feature_flag.target_users,
            conditions=feature_flag.conditions,
            expiry_date=feature_flag.expiry_date
        )
        db.add(db_feature_flag)
        db.commit()
        db.refresh(db_feature_flag)
        return FeatureFlagResponse.from_orm(db_feature_flag)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/features", response_model=List[FeatureFlagResponse])
async def get_feature_flags(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_enabled: Optional[bool] = None
):
    """Get all feature flags with optional filters."""
    query = db.query(FeatureFlag)
    
    if is_enabled is not None:
        query = query.filter(FeatureFlag.is_enabled == is_enabled)
    
    feature_flags = query.offset(skip).limit(limit).all()
    return [FeatureFlagResponse.from_orm(flag) for flag in feature_flags]


@router.get("/features/{flag_id}", response_model=FeatureFlagResponse)
async def get_feature_flag(
    flag_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific feature flag by ID."""
    feature_flag = db.query(FeatureFlag).filter(FeatureFlag.id == flag_id).first()
    
    if not feature_flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    return FeatureFlagResponse.from_orm(feature_flag)


@router.get("/features/key/{flag_key}", response_model=FeatureFlagResponse)
async def get_feature_flag_by_key(
    flag_key: str,
    db: Session = Depends(get_db)
):
    """Get a feature flag by key."""
    feature_flag = db.query(FeatureFlag).filter(FeatureFlag.flag_key == flag_key).first()
    
    if not feature_flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    return FeatureFlagResponse.from_orm(feature_flag)


@router.put("/features/{flag_id}", response_model=FeatureFlagResponse)
async def update_feature_flag(
    flag_id: str,
    feature_flag: FeatureFlagUpdate,
    db: Session = Depends(get_db)
):
    """Update a feature flag."""
    db_feature_flag = db.query(FeatureFlag).filter(FeatureFlag.id == flag_id).first()
    
    if not db_feature_flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    for field, value in feature_flag.dict(exclude_unset=True).items():
        setattr(db_feature_flag, field, value)
    
    db_feature_flag.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_feature_flag)
    return FeatureFlagResponse.from_orm(db_feature_flag)


@router.delete("/features/{flag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feature_flag(
    flag_id: str,
    db: Session = Depends(get_db)
):
    """Delete a feature flag."""
    feature_flag = db.query(FeatureFlag).filter(FeatureFlag.id == flag_id).first()
    
    if not feature_flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    db.delete(feature_flag)
    db.commit()


# Environment Configuration Management
@router.post("/environments", response_model=EnvironmentConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_environment_config(
    env_config: EnvironmentConfigCreate,
    db: Session = Depends(get_db)
):
    """Create a new environment configuration."""
    try:
        db_env_config = EnvironmentConfig(
            environment_name=env_config.environment_name,
            environment_type=env_config.environment_type,
            config_data=env_config.config_data,
            variables=env_config.variables,
            secrets=env_config.secrets,
            description=env_config.description
        )
        db.add(db_env_config)
        db.commit()
        db.refresh(db_env_config)
        return EnvironmentConfigResponse.from_orm(db_env_config)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/environments", response_model=List[EnvironmentConfigResponse])
async def get_environment_configs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    environment_type: Optional[str] = None
):
    """Get all environment configurations with optional filters."""
    query = db.query(EnvironmentConfig)
    
    if environment_type:
        query = query.filter(EnvironmentConfig.environment_type == environment_type)
    
    env_configs = query.offset(skip).limit(limit).all()
    return [EnvironmentConfigResponse.from_orm(config) for config in env_configs]


@router.get("/environments/{env_id}", response_model=EnvironmentConfigResponse)
async def get_environment_config(
    env_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific environment configuration by ID."""
    env_config = db.query(EnvironmentConfig).filter(EnvironmentConfig.id == env_id).first()
    
    if not env_config:
        raise HTTPException(status_code=404, detail="Environment configuration not found")
    
    return EnvironmentConfigResponse.from_orm(env_config)


@router.put("/environments/{env_id}", response_model=EnvironmentConfigResponse)
async def update_environment_config(
    env_id: str,
    env_config: EnvironmentConfigUpdate,
    db: Session = Depends(get_db)
):
    """Update an environment configuration."""
    db_env_config = db.query(EnvironmentConfig).filter(EnvironmentConfig.id == env_id).first()
    
    if not db_env_config:
        raise HTTPException(status_code=404, detail="Environment configuration not found")
    
    for field, value in env_config.dict(exclude_unset=True).items():
        setattr(db_env_config, field, value)
    
    db_env_config.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_env_config)
    return EnvironmentConfigResponse.from_orm(db_env_config)


@router.delete("/environments/{env_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_environment_config(
    env_id: str,
    db: Session = Depends(get_db)
):
    """Delete an environment configuration."""
    env_config = db.query(EnvironmentConfig).filter(EnvironmentConfig.id == env_id).first()
    
    if not env_config:
        raise HTTPException(status_code=404, detail="Environment configuration not found")
    
    db.delete(env_config)
    db.commit()


# Service Configuration Management
@router.post("/services", response_model=ServiceConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_service_config(
    service_config: ServiceConfigCreate,
    db: Session = Depends(get_db)
):
    """Create a new service configuration."""
    try:
        db_service_config = ServiceConfig(
            service_name=service_config.service_name,
            service_type=service_config.service_type,
            config_data=service_config.config_data,
            endpoints=service_config.endpoints,
            health_check_url=service_config.health_check_url,
            timeout=service_config.timeout,
            retry_config=service_config.retry_config,
            circuit_breaker_config=service_config.circuit_breaker_config
        )
        db.add(db_service_config)
        db.commit()
        db.refresh(db_service_config)
        return ServiceConfigResponse.from_orm(db_service_config)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/services", response_model=List[ServiceConfigResponse])
async def get_service_configs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service_type: Optional[str] = None
):
    """Get all service configurations with optional filters."""
    query = db.query(ServiceConfig)
    
    if service_type:
        query = query.filter(ServiceConfig.service_type == service_type)
    
    service_configs = query.offset(skip).limit(limit).all()
    return [ServiceConfigResponse.from_orm(config) for config in service_configs]


@router.get("/services/{service_id}", response_model=ServiceConfigResponse)
async def get_service_config(
    service_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific service configuration by ID."""
    service_config = db.query(ServiceConfig).filter(ServiceConfig.id == service_id).first()
    
    if not service_config:
        raise HTTPException(status_code=404, detail="Service configuration not found")
    
    return ServiceConfigResponse.from_orm(service_config)


@router.put("/services/{service_id}", response_model=ServiceConfigResponse)
async def update_service_config(
    service_id: str,
    service_config: ServiceConfigUpdate,
    db: Session = Depends(get_db)
):
    """Update a service configuration."""
    db_service_config = db.query(ServiceConfig).filter(ServiceConfig.id == service_id).first()
    
    if not db_service_config:
        raise HTTPException(status_code=404, detail="Service configuration not found")
    
    for field, value in service_config.dict(exclude_unset=True).items():
        setattr(db_service_config, field, value)
    
    db_service_config.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_service_config)
    return ServiceConfigResponse.from_orm(db_service_config)


@router.delete("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_config(
    service_id: str,
    db: Session = Depends(get_db)
):
    """Delete a service configuration."""
    service_config = db.query(ServiceConfig).filter(ServiceConfig.id == service_id).first()
    
    if not service_config:
        raise HTTPException(status_code=404, detail="Service configuration not found")
    
    db.delete(service_config)
    db.commit()


# Configuration Template Management
@router.post("/templates", response_model=ConfigTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_config_template(
    template: ConfigTemplateCreate,
    db: Session = Depends(get_db)
):
    """Create a new configuration template."""
    try:
        db_template = ConfigTemplate(
            template_name=template.template_name,
            template_type=template.template_type,
            template_data=template.template_data,
            variables=template.variables,
            description=template.description,
            version=template.version
        )
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        return ConfigTemplateResponse.from_orm(db_template)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/templates", response_model=List[ConfigTemplateResponse])
async def get_config_templates(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    template_type: Optional[str] = None
):
    """Get all configuration templates with optional filters."""
    query = db.query(ConfigTemplate)
    
    if template_type:
        query = query.filter(ConfigTemplate.template_type == template_type)
    
    templates = query.offset(skip).limit(limit).all()
    return [ConfigTemplateResponse.from_orm(template) for template in templates]


@router.get("/templates/{template_id}", response_model=ConfigTemplateResponse)
async def get_config_template(
    template_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific configuration template by ID."""
    template = db.query(ConfigTemplate).filter(ConfigTemplate.id == template_id).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Configuration template not found")
    
    return ConfigTemplateResponse.from_orm(template)


@router.put("/templates/{template_id}", response_model=ConfigTemplateResponse)
async def update_config_template(
    template_id: str,
    template: ConfigTemplateUpdate,
    db: Session = Depends(get_db)
):
    """Update a configuration template."""
    db_template = db.query(ConfigTemplate).filter(ConfigTemplate.id == template_id).first()
    
    if not db_template:
        raise HTTPException(status_code=404, detail="Configuration template not found")
    
    for field, value in template.dict(exclude_unset=True).items():
        setattr(db_template, field, value)
    
    db_template.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_template)
    return ConfigTemplateResponse.from_orm(db_template)


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_config_template(
    template_id: str,
    db: Session = Depends(get_db)
):
    """Delete a configuration template."""
    template = db.query(ConfigTemplate).filter(ConfigTemplate.id == template_id).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Configuration template not found")
    
    db.delete(template)
    db.commit()


# Configuration Override Management
@router.post("/overrides", response_model=ConfigOverrideResponse, status_code=status.HTTP_201_CREATED)
async def create_config_override(
    override: ConfigOverrideCreate,
    db: Session = Depends(get_db)
):
    """Create a new configuration override."""
    try:
        db_override = ConfigOverride(
            tenant_id=override.tenant_id,
            config_key=override.config_key,
            config_value=override.config_value,
            override_type=override.override_type,
            priority=override.priority,
            conditions=override.conditions,
            description=override.description
        )
        db.add(db_override)
        db.commit()
        db.refresh(db_override)
        return ConfigOverrideResponse.from_orm(db_override)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/overrides", response_model=List[ConfigOverrideResponse])
async def get_config_overrides(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    override_type: Optional[str] = None
):
    """Get all configuration overrides with optional filters."""
    query = db.query(ConfigOverride)
    
    if tenant_id:
        query = query.filter(ConfigOverride.tenant_id == tenant_id)
    if override_type:
        query = query.filter(ConfigOverride.override_type == override_type)
    
    overrides = query.offset(skip).limit(limit).all()
    return [ConfigOverrideResponse.from_orm(override) for override in overrides]


@router.get("/overrides/{override_id}", response_model=ConfigOverrideResponse)
async def get_config_override(
    override_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific configuration override by ID."""
    override = db.query(ConfigOverride).filter(ConfigOverride.id == override_id).first()
    
    if not override:
        raise HTTPException(status_code=404, detail="Configuration override not found")
    
    return ConfigOverrideResponse.from_orm(override)


@router.put("/overrides/{override_id}", response_model=ConfigOverrideResponse)
async def update_config_override(
    override_id: str,
    override: ConfigOverrideUpdate,
    db: Session = Depends(get_db)
):
    """Update a configuration override."""
    db_override = db.query(ConfigOverride).filter(ConfigOverride.id == override_id).first()
    
    if not db_override:
        raise HTTPException(status_code=404, detail="Configuration override not found")
    
    for field, value in override.dict(exclude_unset=True).items():
        setattr(db_override, field, value)
    
    db_override.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_override)
    return ConfigOverrideResponse.from_orm(db_override)


@router.delete("/overrides/{override_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_config_override(
    override_id: str,
    db: Session = Depends(get_db)
):
    """Delete a configuration override."""
    override = db.query(ConfigOverride).filter(ConfigOverride.id == override_id).first()
    
    if not override:
        raise HTTPException(status_code=404, detail="Configuration override not found")
    
    db.delete(override)
    db.commit()


# Health Check
@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "config-service",
        "timestamp": datetime.utcnow().isoformat()
    } 
"""
SQLAlchemy models for Transport Service (AI SchoolOS)
"""

from datetime import datetime, date, time
import uuid
import json
from sqlalchemy import (
    Column, String, DateTime, Boolean, ForeignKey, Table, Index, Text, Integer, Date, Float, Numeric
)
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
from sqlalchemy.types import TypeDecorator, Text

Base = declarative_base()

class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string."""
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class UUIDString(TypeDecorator):
    """Custom UUID type that works with both PostgreSQL and SQLite."""
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return str(value)  # Keep as string to avoid UUID object issues
        return value


class Vehicle(Base):
    __tablename__ = "vehicles"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Vehicle Information
    vehicle_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    vehicle_type: Mapped[str] = mapped_column(String(50), nullable=False)  # bus, van, car, minibus
    vehicle_model: Mapped[str] = mapped_column(String(100), nullable=True)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=True)
    year_of_manufacture: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Capacity and Features
    seating_capacity: Mapped[int] = mapped_column(Integer, default=30)
    standing_capacity: Mapped[int] = mapped_column(Integer, default=10)
    total_capacity: Mapped[int] = mapped_column(Integer, default=40)
    features: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # AC, GPS, CCTV, etc.
    
    # Registration and Insurance
    registration_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    insurance_number: Mapped[str] = mapped_column(String(100), nullable=True)
    insurance_expiry: Mapped[date] = mapped_column(Date, nullable=True)
    permit_number: Mapped[str] = mapped_column(String(100), nullable=True)
    permit_expiry: Mapped[date] = mapped_column(Date, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    is_under_maintenance: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_vehicles_tenant_id", "tenant_id"),
        Index("ix_vehicles_vehicle_number", "vehicle_number"),
        Index("ix_vehicles_registration_number", "registration_number"),
        Index("ix_vehicles_is_active", "is_active"),
    )


class Driver(Base):
    __tablename__ = "drivers"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Driver Information
    driver_id: Mapped[str] = mapped_column(UUIDString, nullable=False)  # Reference to staff service
    driver_name: Mapped[str] = mapped_column(String(100), nullable=False)
    driver_code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    
    # Contact Information
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    
    # License Information
    license_number: Mapped[str] = mapped_column(String(50), nullable=False)
    license_type: Mapped[str] = mapped_column(String(20), nullable=False)  # LMV, HMV, etc.
    license_expiry: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Experience and Skills
    experience_years: Mapped[int] = mapped_column(Integer, default=0)
    skills: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    certifications: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_drivers_tenant_id", "tenant_id"),
        Index("ix_drivers_driver_code", "driver_code"),
        Index("ix_drivers_license_number", "license_number"),
        Index("ix_drivers_is_active", "is_active"),
    )


class Route(Base):
    __tablename__ = "routes"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Route Information
    route_name: Mapped[str] = mapped_column(String(100), nullable=False)
    route_code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    route_type: Mapped[str] = mapped_column(String(50), nullable=False)  # pickup, drop, circular
    
    # Route Details
    start_location: Mapped[str] = mapped_column(String(200), nullable=False)
    end_location: Mapped[str] = mapped_column(String(200), nullable=False)
    total_distance: Mapped[float] = mapped_column(Float, default=0.0)  # in kilometers
    estimated_duration: Mapped[int] = mapped_column(Integer, default=0)  # in minutes
    
    # Route Path
    route_path: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # GPS coordinates
    waypoints: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_routes_tenant_id", "tenant_id"),
        Index("ix_routes_route_code", "route_code"),
        Index("ix_routes_route_type", "route_type"),
        Index("ix_routes_is_active", "is_active"),
    )


class Stop(Base):
    __tablename__ = "stops"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Stop Information
    stop_name: Mapped[str] = mapped_column(String(100), nullable=False)
    stop_code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    stop_type: Mapped[str] = mapped_column(String(50), nullable=False)  # pickup, drop, both
    
    # Location Information
    address: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    landmark: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # Stop Details
    waiting_time: Mapped[int] = mapped_column(Integer, default=2)  # minutes
    is_safe_stop: Mapped[bool] = mapped_column(Boolean, default=True)
    facilities: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_stops_tenant_id", "tenant_id"),
        Index("ix_stops_stop_code", "stop_code"),
        Index("ix_stops_stop_type", "stop_type"),
        Index("ix_stops_is_active", "is_active"),
    )


class RouteStop(Base):
    __tablename__ = "route_stops"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Route and Stop Information
    route_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    stop_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Stop Order and Timing
    stop_order: Mapped[int] = mapped_column(Integer, nullable=False)
    estimated_arrival_time: Mapped[time] = mapped_column(DateTime, nullable=True)
    estimated_departure_time: Mapped[time] = mapped_column(DateTime, nullable=True)
    
    # Distance Information
    distance_from_start: Mapped[float] = mapped_column(Float, default=0.0)
    distance_to_next: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_route_stops_tenant_id", "tenant_id"),
        Index("ix_route_stops_route_id", "route_id"),
        Index("ix_route_stops_stop_id", "stop_id"),
        Index("ix_route_stops_stop_order", "stop_order"),
    )


class TransportSchedule(Base):
    __tablename__ = "transport_schedules"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Schedule Information
    schedule_name: Mapped[str] = mapped_column(String(100), nullable=False)
    route_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    vehicle_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    driver_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Timing Information
    departure_time: Mapped[time] = mapped_column(DateTime, nullable=False)
    arrival_time: Mapped[time] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=0)
    
    # Schedule Details
    schedule_type: Mapped[str] = mapped_column(String(50), nullable=False)  # morning, afternoon, evening
    days_of_week: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_transport_schedules_tenant_id", "tenant_id"),
        Index("ix_transport_schedules_route_id", "route_id"),
        Index("ix_transport_schedules_vehicle_id", "vehicle_id"),
        Index("ix_transport_schedules_driver_id", "driver_id"),
        Index("ix_transport_schedules_schedule_type", "schedule_type"),
    )


class TransportBooking(Base):
    __tablename__ = "transport_bookings"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Booking Information
    student_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    schedule_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    pickup_stop_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    drop_stop_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Booking Details
    booking_date: Mapped[date] = mapped_column(Date, nullable=False)
    booking_type: Mapped[str] = mapped_column(String(50), nullable=False)  # daily, monthly, yearly
    fare_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    
    # Status
    booking_status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, confirmed, cancelled
    payment_status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, paid, refunded
    
    # Additional Information
    special_requirements: Mapped[str] = mapped_column(Text, nullable=True)
    parent_contact: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_transport_bookings_tenant_id", "tenant_id"),
        Index("ix_transport_bookings_student_id", "student_id"),
        Index("ix_transport_bookings_schedule_id", "schedule_id"),
        Index("ix_transport_bookings_booking_status", "booking_status"),
    )


class VehicleTracking(Base):
    __tablename__ = "vehicle_tracking"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Tracking Information
    vehicle_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    schedule_id: Mapped[str] = mapped_column(UUIDString, nullable=True)
    driver_id: Mapped[str] = mapped_column(UUIDString, nullable=True)
    
    # Location Information
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    altitude: Mapped[float] = mapped_column(Float, nullable=True)
    speed: Mapped[float] = mapped_column(Float, nullable=True)  # km/h
    heading: Mapped[float] = mapped_column(Float, nullable=True)  # degrees
    
    # Status Information
    engine_status: Mapped[str] = mapped_column(String(20), nullable=True)  # running, stopped
    fuel_level: Mapped[float] = mapped_column(Float, nullable=True)  # percentage
    temperature: Mapped[float] = mapped_column(Float, nullable=True)  # celsius
    
    # Timestamps
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_vehicle_tracking_tenant_id", "tenant_id"),
        Index("ix_vehicle_tracking_vehicle_id", "vehicle_id"),
        Index("ix_vehicle_tracking_timestamp", "timestamp"),
    )


class TransportIncident(Base):
    __tablename__ = "transport_incidents"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Incident Information
    incident_type: Mapped[str] = mapped_column(String(50), nullable=False)  # accident, breakdown, delay, other
    incident_severity: Mapped[str] = mapped_column(String(20), nullable=False)  # low, medium, high, critical
    
    # Involved Parties
    vehicle_id: Mapped[str] = mapped_column(UUIDString, nullable=True)
    driver_id: Mapped[str] = mapped_column(UUIDString, nullable=True)
    schedule_id: Mapped[str] = mapped_column(UUIDString, nullable=True)
    
    # Incident Details
    incident_date: Mapped[date] = mapped_column(Date, nullable=False)
    incident_time: Mapped[time] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    
    # Description and Impact
    description: Mapped[str] = mapped_column(Text, nullable=False)
    impact_assessment: Mapped[str] = mapped_column(Text, nullable=True)
    affected_students: Mapped[int] = mapped_column(Integer, default=0)
    
    # Resolution
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolution_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    resolution_notes: Mapped[str] = mapped_column(Text, nullable=True)
    resolved_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_transport_incidents_tenant_id", "tenant_id"),
        Index("ix_transport_incidents_incident_type", "incident_type"),
        Index("ix_transport_incidents_incident_severity", "incident_severity"),
        Index("ix_transport_incidents_is_resolved", "is_resolved"),
    ) 
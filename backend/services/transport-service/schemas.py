"""
Pydantic schemas for Transport Service (AI SchoolOS)
"""

from datetime import datetime, date, time
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from sqlalchemy.orm import Query


# Base schemas
class VehicleBase(BaseModel):
    vehicle_number: str = Field(..., description="Vehicle number/identifier")
    vehicle_type: str = Field(..., description="Type of vehicle (bus, van, car, minibus)")
    vehicle_model: Optional[str] = Field(None, description="Vehicle model")
    manufacturer: Optional[str] = Field(None, description="Vehicle manufacturer")
    year_of_manufacture: Optional[int] = Field(None, description="Year of manufacture")
    seating_capacity: int = Field(30, description="Seating capacity")
    standing_capacity: int = Field(10, description="Standing capacity")
    total_capacity: int = Field(40, description="Total capacity")
    features: Dict[str, Any] = Field(default_factory=dict, description="Vehicle features")
    registration_number: str = Field(..., description="Vehicle registration number")
    insurance_number: Optional[str] = Field(None, description="Insurance number")
    insurance_expiry: Optional[date] = Field(None, description="Insurance expiry date")
    permit_number: Optional[str] = Field(None, description="Permit number")
    permit_expiry: Optional[date] = Field(None, description="Permit expiry date")


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    vehicle_number: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_model: Optional[str] = None
    manufacturer: Optional[str] = None
    year_of_manufacture: Optional[int] = None
    seating_capacity: Optional[int] = None
    standing_capacity: Optional[int] = None
    total_capacity: Optional[int] = None
    features: Optional[Dict[str, Any]] = None
    registration_number: Optional[str] = None
    insurance_number: Optional[str] = None
    insurance_expiry: Optional[date] = None
    permit_number: Optional[str] = None
    permit_expiry: Optional[date] = None
    is_active: Optional[bool] = None
    is_available: Optional[bool] = None
    is_under_maintenance: Optional[bool] = None


class VehicleResponse(VehicleBase):
    id: str
    tenant_id: str
    is_active: bool
    is_available: bool
    is_under_maintenance: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Driver schemas
class DriverBase(BaseModel):
    driver_id: str = Field(..., description="Reference to staff service")
    driver_name: str = Field(..., description="Driver name")
    driver_code: str = Field(..., description="Driver code")
    phone_number: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email address")
    address: Optional[str] = Field(None, description="Address")
    license_number: str = Field(..., description="License number")
    license_type: str = Field(..., description="License type (LMV, HMV, etc.)")
    license_expiry: date = Field(..., description="License expiry date")
    experience_years: int = Field(0, description="Years of experience")
    skills: Dict[str, Any] = Field(default_factory=dict, description="Driver skills")
    certifications: Dict[str, Any] = Field(default_factory=dict, description="Driver certifications")


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    driver_id: Optional[str] = None
    driver_name: Optional[str] = None
    driver_code: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    license_number: Optional[str] = None
    license_type: Optional[str] = None
    license_expiry: Optional[date] = None
    experience_years: Optional[int] = None
    skills: Optional[Dict[str, Any]] = None
    certifications: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_available: Optional[bool] = None


class DriverResponse(DriverBase):
    id: str
    tenant_id: str
    is_active: bool
    is_available: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Route schemas
class RouteBase(BaseModel):
    route_name: str = Field(..., description="Route name")
    route_code: str = Field(..., description="Route code")
    route_type: str = Field(..., description="Route type (pickup, drop, circular)")
    start_location: str = Field(..., description="Start location")
    end_location: str = Field(..., description="End location")
    total_distance: float = Field(0.0, description="Total distance in kilometers")
    estimated_duration: int = Field(0, description="Estimated duration in minutes")
    route_path: Dict[str, Any] = Field(default_factory=dict, description="GPS coordinates")
    waypoints: Dict[str, Any] = Field(default_factory=dict, description="Waypoints")
    is_default: bool = Field(False, description="Is default route")


class RouteCreate(RouteBase):
    pass


class RouteUpdate(BaseModel):
    route_name: Optional[str] = None
    route_code: Optional[str] = None
    route_type: Optional[str] = None
    start_location: Optional[str] = None
    end_location: Optional[str] = None
    total_distance: Optional[float] = None
    estimated_duration: Optional[int] = None
    route_path: Optional[Dict[str, Any]] = None
    waypoints: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None


class RouteResponse(RouteBase):
    id: str
    tenant_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Stop schemas
class StopBase(BaseModel):
    stop_name: str = Field(..., description="Stop name")
    stop_code: str = Field(..., description="Stop code")
    stop_type: str = Field(..., description="Stop type (pickup, drop, both)")
    address: str = Field(..., description="Stop address")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")
    landmark: Optional[str] = Field(None, description="Landmark")
    waiting_time: int = Field(2, description="Waiting time in minutes")
    is_safe_stop: bool = Field(True, description="Is safe stop")
    facilities: Dict[str, Any] = Field(default_factory=dict, description="Stop facilities")


class StopCreate(StopBase):
    pass


class StopUpdate(BaseModel):
    stop_name: Optional[str] = None
    stop_code: Optional[str] = None
    stop_type: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    landmark: Optional[str] = None
    waiting_time: Optional[int] = None
    is_safe_stop: Optional[bool] = None
    facilities: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class StopResponse(StopBase):
    id: str
    tenant_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Transport Schedule schemas
class TransportScheduleBase(BaseModel):
    schedule_name: str = Field(..., description="Schedule name")
    route_id: str = Field(..., description="Route ID")
    vehicle_id: str = Field(..., description="Vehicle ID")
    driver_id: str = Field(..., description="Driver ID")
    departure_time: time = Field(..., description="Departure time")
    arrival_time: time = Field(..., description="Arrival time")
    duration_minutes: int = Field(0, description="Duration in minutes")
    schedule_type: str = Field(..., description="Schedule type (morning, afternoon, evening)")
    days_of_week: Dict[str, Any] = Field(default_factory=dict, description="Days of week")
    academic_year: str = Field(..., description="Academic year")
    is_recurring: bool = Field(True, description="Is recurring schedule")


class TransportScheduleCreate(TransportScheduleBase):
    pass


class TransportScheduleUpdate(BaseModel):
    schedule_name: Optional[str] = None
    route_id: Optional[str] = None
    vehicle_id: Optional[str] = None
    driver_id: Optional[str] = None
    departure_time: Optional[time] = None
    arrival_time: Optional[time] = None
    duration_minutes: Optional[int] = None
    schedule_type: Optional[str] = None
    days_of_week: Optional[Dict[str, Any]] = None
    academic_year: Optional[str] = None
    is_active: Optional[bool] = None
    is_recurring: Optional[bool] = None


class TransportScheduleResponse(TransportScheduleBase):
    id: str
    tenant_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Transport Booking schemas
class TransportBookingBase(BaseModel):
    student_id: str = Field(..., description="Student ID")
    schedule_id: str = Field(..., description="Schedule ID")
    pickup_stop_id: str = Field(..., description="Pickup stop ID")
    drop_stop_id: str = Field(..., description="Drop stop ID")
    booking_date: date = Field(..., description="Booking date")
    booking_type: str = Field(..., description="Booking type (daily, monthly, yearly)")
    fare_amount: float = Field(0.0, description="Fare amount")
    special_requirements: Optional[str] = Field(None, description="Special requirements")
    parent_contact: Optional[str] = Field(None, description="Parent contact")


class TransportBookingCreate(TransportBookingBase):
    pass


class TransportBookingUpdate(BaseModel):
    student_id: Optional[str] = None
    schedule_id: Optional[str] = None
    pickup_stop_id: Optional[str] = None
    drop_stop_id: Optional[str] = None
    booking_date: Optional[date] = None
    booking_type: Optional[str] = None
    fare_amount: Optional[float] = None
    booking_status: Optional[str] = None
    payment_status: Optional[str] = None
    special_requirements: Optional[str] = None
    parent_contact: Optional[str] = None


class TransportBookingResponse(TransportBookingBase):
    id: str
    tenant_id: str
    booking_status: str
    payment_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Vehicle Tracking schemas
class VehicleTrackingBase(BaseModel):
    vehicle_id: str = Field(..., description="Vehicle ID")
    schedule_id: Optional[str] = Field(None, description="Schedule ID")
    driver_id: Optional[str] = Field(None, description="Driver ID")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    altitude: Optional[float] = Field(None, description="Altitude")
    speed: Optional[float] = Field(None, description="Speed in km/h")
    heading: Optional[float] = Field(None, description="Heading in degrees")
    engine_status: Optional[str] = Field(None, description="Engine status")
    fuel_level: Optional[float] = Field(None, description="Fuel level percentage")
    temperature: Optional[float] = Field(None, description="Temperature in celsius")
    timestamp: Optional[datetime] = Field(None, description="Tracking timestamp")


class VehicleTrackingCreate(VehicleTrackingBase):
    pass


class VehicleTrackingResponse(VehicleTrackingBase):
    id: str
    tenant_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# Transport Incident schemas
class TransportIncidentBase(BaseModel):
    incident_type: str = Field(..., description="Incident type (accident, breakdown, delay, other)")
    incident_severity: str = Field(..., description="Incident severity (low, medium, high, critical)")
    vehicle_id: Optional[str] = Field(None, description="Vehicle ID")
    driver_id: Optional[str] = Field(None, description="Driver ID")
    schedule_id: Optional[str] = Field(None, description="Schedule ID")
    incident_date: date = Field(..., description="Incident date")
    incident_time: time = Field(..., description="Incident time")
    location: Optional[str] = Field(None, description="Incident location")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")
    description: str = Field(..., description="Incident description")
    impact_assessment: Optional[str] = Field(None, description="Impact assessment")
    affected_students: int = Field(0, description="Number of affected students")


class TransportIncidentCreate(TransportIncidentBase):
    pass


class TransportIncidentUpdate(BaseModel):
    incident_type: Optional[str] = None
    incident_severity: Optional[str] = None
    vehicle_id: Optional[str] = None
    driver_id: Optional[str] = None
    schedule_id: Optional[str] = None
    incident_date: Optional[date] = None
    incident_time: Optional[time] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    impact_assessment: Optional[str] = None
    affected_students: Optional[int] = None
    is_resolved: Optional[bool] = None
    resolution_date: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    resolved_by: Optional[str] = None


class TransportIncidentResponse(TransportIncidentBase):
    id: str
    tenant_id: str
    is_resolved: bool
    resolution_date: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    resolved_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Health check response
class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str 
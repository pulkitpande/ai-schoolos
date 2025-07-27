"""
Transport Service Router

Handles all transport-related operations including vehicles, drivers, routes, schedules, and bookings.
"""

from datetime import datetime, date, time
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from database import get_db
from models import (
    Vehicle, Driver, Route, Stop, RouteStop, TransportSchedule, 
    TransportBooking, VehicleTracking, TransportIncident
)
from schemas import (
    VehicleCreate, VehicleUpdate, VehicleResponse,
    DriverCreate, DriverUpdate, DriverResponse,
    RouteCreate, RouteUpdate, RouteResponse,
    StopCreate, StopUpdate, StopResponse,
    TransportScheduleCreate, TransportScheduleUpdate, TransportScheduleResponse,
    TransportBookingCreate, TransportBookingUpdate, TransportBookingResponse,
    VehicleTrackingCreate, VehicleTrackingResponse,
    TransportIncidentCreate, TransportIncidentUpdate, TransportIncidentResponse
)

router = APIRouter(prefix="/transport", tags=["transport"])


@router.get("/")
async def root():
    return {"message": "Transport Service is running"}


# Vehicle Management
@router.post("/vehicles", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new vehicle."""
    try:
        db_vehicle = Vehicle(
            tenant_id=tenant_id,
            vehicle_number=vehicle.vehicle_number,
            vehicle_type=vehicle.vehicle_type,
            vehicle_model=vehicle.vehicle_model,
            manufacturer=vehicle.manufacturer,
            year_of_manufacture=vehicle.year_of_manufacture,
            seating_capacity=vehicle.seating_capacity,
            standing_capacity=vehicle.standing_capacity,
            total_capacity=vehicle.total_capacity,
            features=vehicle.features,
            registration_number=vehicle.registration_number,
            insurance_number=vehicle.insurance_number,
            insurance_expiry=vehicle.insurance_expiry,
            permit_number=vehicle.permit_number,
            permit_expiry=vehicle.permit_expiry
        )
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return VehicleResponse.from_orm(db_vehicle)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/vehicles", response_model=List[VehicleResponse])
async def get_vehicles(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    vehicle_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_available: Optional[bool] = None
):
    """Get all vehicles with optional filters."""
    query = db.query(Vehicle).filter(Vehicle.tenant_id == tenant_id)
    
    if vehicle_type:
        query = query.filter(Vehicle.vehicle_type == vehicle_type)
    if is_active is not None:
        query = query.filter(Vehicle.is_active == is_active)
    if is_available is not None:
        query = query.filter(Vehicle.is_available == is_available)
    
    vehicles = query.offset(skip).limit(limit).all()
    return [VehicleResponse.from_orm(vehicle) for vehicle in vehicles]


@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific vehicle by ID."""
    vehicle = db.query(Vehicle).filter(
        and_(Vehicle.id == vehicle_id, Vehicle.tenant_id == tenant_id)
    ).first()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    return VehicleResponse.from_orm(vehicle)


@router.put("/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: str,
    vehicle: VehicleUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update a vehicle."""
    db_vehicle = db.query(Vehicle).filter(
        and_(Vehicle.id == vehicle_id, Vehicle.tenant_id == tenant_id)
    ).first()
    
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    for field, value in vehicle.dict(exclude_unset=True).items():
        setattr(db_vehicle, field, value)
    
    db_vehicle.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_vehicle)
    return VehicleResponse.from_orm(db_vehicle)


@router.delete("/vehicles/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete a vehicle (soft delete)."""
    vehicle = db.query(Vehicle).filter(
        and_(Vehicle.id == vehicle_id, Vehicle.tenant_id == tenant_id)
    ).first()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    vehicle.is_active = False
    vehicle.updated_at = datetime.utcnow()
    db.commit()


# Driver Management
@router.post("/drivers", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
async def create_driver(
    driver: DriverCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new driver."""
    try:
        db_driver = Driver(
            tenant_id=tenant_id,
            driver_id=driver.driver_id,
            driver_name=driver.driver_name,
            driver_code=driver.driver_code,
            phone_number=driver.phone_number,
            email=driver.email,
            address=driver.address,
            license_number=driver.license_number,
            license_type=driver.license_type,
            license_expiry=driver.license_expiry,
            experience_years=driver.experience_years,
            skills=driver.skills,
            certifications=driver.certifications
        )
        db.add(db_driver)
        db.commit()
        db.refresh(db_driver)
        return DriverResponse.from_orm(db_driver)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/drivers", response_model=List[DriverResponse])
async def get_drivers(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None,
    is_available: Optional[bool] = None
):
    """Get all drivers with optional filters."""
    query = db.query(Driver).filter(Driver.tenant_id == tenant_id)
    
    if is_active is not None:
        query = query.filter(Driver.is_active == is_active)
    if is_available is not None:
        query = query.filter(Driver.is_available == is_available)
    
    drivers = query.offset(skip).limit(limit).all()
    return [DriverResponse.from_orm(driver) for driver in drivers]


@router.get("/drivers/{driver_id}", response_model=DriverResponse)
async def get_driver(
    driver_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific driver by ID."""
    driver = db.query(Driver).filter(
        and_(Driver.id == driver_id, Driver.tenant_id == tenant_id)
    ).first()
    
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    return DriverResponse.from_orm(driver)


@router.put("/drivers/{driver_id}", response_model=DriverResponse)
async def update_driver(
    driver_id: str,
    driver: DriverUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update a driver."""
    db_driver = db.query(Driver).filter(
        and_(Driver.id == driver_id, Driver.tenant_id == tenant_id)
    ).first()
    
    if not db_driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    for field, value in driver.dict(exclude_unset=True).items():
        setattr(db_driver, field, value)
    
    db_driver.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_driver)
    return DriverResponse.from_orm(db_driver)


@router.delete("/drivers/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_driver(
    driver_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete a driver (soft delete)."""
    driver = db.query(Driver).filter(
        and_(Driver.id == driver_id, Driver.tenant_id == tenant_id)
    ).first()
    
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    driver.is_active = False
    driver.updated_at = datetime.utcnow()
    db.commit()


# Route Management
@router.post("/routes", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
async def create_route(
    route: RouteCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new route."""
    try:
        db_route = Route(
            tenant_id=tenant_id,
            route_name=route.route_name,
            route_code=route.route_code,
            route_type=route.route_type,
            start_location=route.start_location,
            end_location=route.end_location,
            total_distance=route.total_distance,
            estimated_duration=route.estimated_duration,
            route_path=route.route_path,
            waypoints=route.waypoints,
            is_default=route.is_default
        )
        db.add(db_route)
        db.commit()
        db.refresh(db_route)
        return RouteResponse.from_orm(db_route)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/routes", response_model=List[RouteResponse])
async def get_routes(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    route_type: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """Get all routes with optional filters."""
    query = db.query(Route).filter(Route.tenant_id == tenant_id)
    
    if route_type:
        query = query.filter(Route.route_type == route_type)
    if is_active is not None:
        query = query.filter(Route.is_active == is_active)
    
    routes = query.offset(skip).limit(limit).all()
    return [RouteResponse.from_orm(route) for route in routes]


@router.get("/routes/{route_id}", response_model=RouteResponse)
async def get_route(
    route_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific route by ID."""
    route = db.query(Route).filter(
        and_(Route.id == route_id, Route.tenant_id == tenant_id)
    ).first()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    return RouteResponse.from_orm(route)


@router.put("/routes/{route_id}", response_model=RouteResponse)
async def update_route(
    route_id: str,
    route: RouteUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update a route."""
    db_route = db.query(Route).filter(
        and_(Route.id == route_id, Route.tenant_id == tenant_id)
    ).first()
    
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    for field, value in route.dict(exclude_unset=True).items():
        setattr(db_route, field, value)
    
    db_route.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_route)
    return RouteResponse.from_orm(db_route)


@router.delete("/routes/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(
    route_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete a route (soft delete)."""
    route = db.query(Route).filter(
        and_(Route.id == route_id, Route.tenant_id == tenant_id)
    ).first()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    route.is_active = False
    route.updated_at = datetime.utcnow()
    db.commit()


# Stop Management
@router.post("/stops", response_model=StopResponse, status_code=status.HTTP_201_CREATED)
async def create_stop(
    stop: StopCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new stop."""
    try:
        db_stop = Stop(
            tenant_id=tenant_id,
            stop_name=stop.stop_name,
            stop_code=stop.stop_code,
            stop_type=stop.stop_type,
            address=stop.address,
            latitude=stop.latitude,
            longitude=stop.longitude,
            landmark=stop.landmark,
            waiting_time=stop.waiting_time,
            is_safe_stop=stop.is_safe_stop,
            facilities=stop.facilities
        )
        db.add(db_stop)
        db.commit()
        db.refresh(db_stop)
        return StopResponse.from_orm(db_stop)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stops", response_model=List[StopResponse])
async def get_stops(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    stop_type: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """Get all stops with optional filters."""
    query = db.query(Stop).filter(Stop.tenant_id == tenant_id)
    
    if stop_type:
        query = query.filter(Stop.stop_type == stop_type)
    if is_active is not None:
        query = query.filter(Stop.is_active == is_active)
    
    stops = query.offset(skip).limit(limit).all()
    return [StopResponse.from_orm(stop) for stop in stops]


@router.get("/stops/{stop_id}", response_model=StopResponse)
async def get_stop(
    stop_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific stop by ID."""
    stop = db.query(Stop).filter(
        and_(Stop.id == stop_id, Stop.tenant_id == tenant_id)
    ).first()
    
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    
    return StopResponse.from_orm(stop)


@router.put("/stops/{stop_id}", response_model=StopResponse)
async def update_stop(
    stop_id: str,
    stop: StopUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update a stop."""
    db_stop = db.query(Stop).filter(
        and_(Stop.id == stop_id, Stop.tenant_id == tenant_id)
    ).first()
    
    if not db_stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    
    for field, value in stop.dict(exclude_unset=True).items():
        setattr(db_stop, field, value)
    
    db_stop.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_stop)
    return StopResponse.from_orm(db_stop)


@router.delete("/stops/{stop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stop(
    stop_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete a stop (soft delete)."""
    stop = db.query(Stop).filter(
        and_(Stop.id == stop_id, Stop.tenant_id == tenant_id)
    ).first()
    
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    
    stop.is_active = False
    stop.updated_at = datetime.utcnow()
    db.commit()


# Transport Schedule Management
@router.post("/schedules", response_model=TransportScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule: TransportScheduleCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new transport schedule."""
    try:
        db_schedule = TransportSchedule(
            tenant_id=tenant_id,
            schedule_name=schedule.schedule_name,
            route_id=schedule.route_id,
            vehicle_id=schedule.vehicle_id,
            driver_id=schedule.driver_id,
            departure_time=schedule.departure_time,
            arrival_time=schedule.arrival_time,
            duration_minutes=schedule.duration_minutes,
            schedule_type=schedule.schedule_type,
            days_of_week=schedule.days_of_week,
            academic_year=schedule.academic_year,
            is_recurring=schedule.is_recurring
        )
        db.add(db_schedule)
        db.commit()
        db.refresh(db_schedule)
        return TransportScheduleResponse.from_orm(db_schedule)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/schedules", response_model=List[TransportScheduleResponse])
async def get_schedules(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    schedule_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    academic_year: Optional[str] = None
):
    """Get all transport schedules with optional filters."""
    query = db.query(TransportSchedule).filter(TransportSchedule.tenant_id == tenant_id)
    
    if schedule_type:
        query = query.filter(TransportSchedule.schedule_type == schedule_type)
    if is_active is not None:
        query = query.filter(TransportSchedule.is_active == is_active)
    if academic_year:
        query = query.filter(TransportSchedule.academic_year == academic_year)
    
    schedules = query.offset(skip).limit(limit).all()
    return [TransportScheduleResponse.from_orm(schedule) for schedule in schedules]


@router.get("/schedules/{schedule_id}", response_model=TransportScheduleResponse)
async def get_schedule(
    schedule_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific transport schedule by ID."""
    schedule = db.query(TransportSchedule).filter(
        and_(TransportSchedule.id == schedule_id, TransportSchedule.tenant_id == tenant_id)
    ).first()
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Transport schedule not found")
    
    return TransportScheduleResponse.from_orm(schedule)


@router.put("/schedules/{schedule_id}", response_model=TransportScheduleResponse)
async def update_schedule(
    schedule_id: str,
    schedule: TransportScheduleUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update a transport schedule."""
    db_schedule = db.query(TransportSchedule).filter(
        and_(TransportSchedule.id == schedule_id, TransportSchedule.tenant_id == tenant_id)
    ).first()
    
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Transport schedule not found")
    
    for field, value in schedule.dict(exclude_unset=True).items():
        setattr(db_schedule, field, value)
    
    db_schedule.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_schedule)
    return TransportScheduleResponse.from_orm(db_schedule)


@router.delete("/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete a transport schedule (soft delete)."""
    schedule = db.query(TransportSchedule).filter(
        and_(TransportSchedule.id == schedule_id, TransportSchedule.tenant_id == tenant_id)
    ).first()
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Transport schedule not found")
    
    schedule.is_active = False
    schedule.updated_at = datetime.utcnow()
    db.commit()


# Transport Booking Management
@router.post("/bookings", response_model=TransportBookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking: TransportBookingCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new transport booking."""
    try:
        db_booking = TransportBooking(
            tenant_id=tenant_id,
            student_id=booking.student_id,
            schedule_id=booking.schedule_id,
            pickup_stop_id=booking.pickup_stop_id,
            drop_stop_id=booking.drop_stop_id,
            booking_date=booking.booking_date,
            booking_type=booking.booking_type,
            fare_amount=booking.fare_amount,
            special_requirements=booking.special_requirements,
            parent_contact=booking.parent_contact
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return TransportBookingResponse.from_orm(db_booking)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/bookings", response_model=List[TransportBookingResponse])
async def get_bookings(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    student_id: Optional[str] = None,
    booking_status: Optional[str] = None,
    payment_status: Optional[str] = None
):
    """Get all transport bookings with optional filters."""
    query = db.query(TransportBooking).filter(TransportBooking.tenant_id == tenant_id)
    
    if student_id:
        query = query.filter(TransportBooking.student_id == student_id)
    if booking_status:
        query = query.filter(TransportBooking.booking_status == booking_status)
    if payment_status:
        query = query.filter(TransportBooking.payment_status == payment_status)
    
    bookings = query.offset(skip).limit(limit).all()
    return [TransportBookingResponse.from_orm(booking) for booking in bookings]


@router.get("/bookings/{booking_id}", response_model=TransportBookingResponse)
async def get_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific transport booking by ID."""
    booking = db.query(TransportBooking).filter(
        and_(TransportBooking.id == booking_id, TransportBooking.tenant_id == tenant_id)
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Transport booking not found")
    
    return TransportBookingResponse.from_orm(booking)


@router.put("/bookings/{booking_id}", response_model=TransportBookingResponse)
async def update_booking(
    booking_id: str,
    booking: TransportBookingUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update a transport booking."""
    db_booking = db.query(TransportBooking).filter(
        and_(TransportBooking.id == booking_id, TransportBooking.tenant_id == tenant_id)
    ).first()
    
    if not db_booking:
        raise HTTPException(status_code=404, detail="Transport booking not found")
    
    for field, value in booking.dict(exclude_unset=True).items():
        setattr(db_booking, field, value)
    
    db_booking.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_booking)
    return TransportBookingResponse.from_orm(db_booking)


@router.delete("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete a transport booking (soft delete)."""
    booking = db.query(TransportBooking).filter(
        and_(TransportBooking.id == booking_id, TransportBooking.tenant_id == tenant_id)
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Transport booking not found")
    
    booking.booking_status = "cancelled"
    booking.updated_at = datetime.utcnow()
    db.commit()


# Vehicle Tracking
@router.post("/tracking", response_model=VehicleTrackingResponse, status_code=status.HTTP_201_CREATED)
async def create_tracking(
    tracking: VehicleTrackingCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new vehicle tracking record."""
    try:
        db_tracking = VehicleTracking(
            tenant_id=tenant_id,
            vehicle_id=tracking.vehicle_id,
            schedule_id=tracking.schedule_id,
            driver_id=tracking.driver_id,
            latitude=tracking.latitude,
            longitude=tracking.longitude,
            altitude=tracking.altitude,
            speed=tracking.speed,
            heading=tracking.heading,
            engine_status=tracking.engine_status,
            fuel_level=tracking.fuel_level,
            temperature=tracking.temperature,
            timestamp=tracking.timestamp or datetime.utcnow()
        )
        db.add(db_tracking)
        db.commit()
        db.refresh(db_tracking)
        return VehicleTrackingResponse.from_orm(db_tracking)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tracking/{vehicle_id}", response_model=List[VehicleTrackingResponse])
async def get_vehicle_tracking(
    vehicle_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get tracking history for a specific vehicle."""
    tracking_records = db.query(VehicleTracking).filter(
        and_(VehicleTracking.vehicle_id == vehicle_id, VehicleTracking.tenant_id == tenant_id)
    ).order_by(VehicleTracking.timestamp.desc()).limit(limit).all()
    
    return [VehicleTrackingResponse.from_orm(record) for record in tracking_records]


# Transport Incidents
@router.post("/incidents", response_model=TransportIncidentResponse, status_code=status.HTTP_201_CREATED)
async def create_incident(
    incident: TransportIncidentCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new transport incident."""
    try:
        db_incident = TransportIncident(
            tenant_id=tenant_id,
            incident_type=incident.incident_type,
            incident_severity=incident.incident_severity,
            vehicle_id=incident.vehicle_id,
            driver_id=incident.driver_id,
            schedule_id=incident.schedule_id,
            incident_date=incident.incident_date,
            incident_time=incident.incident_time,
            location=incident.location,
            latitude=incident.latitude,
            longitude=incident.longitude,
            description=incident.description,
            impact_assessment=incident.impact_assessment,
            affected_students=incident.affected_students
        )
        db.add(db_incident)
        db.commit()
        db.refresh(db_incident)
        return TransportIncidentResponse.from_orm(db_incident)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/incidents", response_model=List[TransportIncidentResponse])
async def get_incidents(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    incident_type: Optional[str] = None,
    incident_severity: Optional[str] = None,
    is_resolved: Optional[bool] = None
):
    """Get all transport incidents with optional filters."""
    query = db.query(TransportIncident).filter(TransportIncident.tenant_id == tenant_id)
    
    if incident_type:
        query = query.filter(TransportIncident.incident_type == incident_type)
    if incident_severity:
        query = query.filter(TransportIncident.incident_severity == incident_severity)
    if is_resolved is not None:
        query = query.filter(TransportIncident.is_resolved == is_resolved)
    
    incidents = query.offset(skip).limit(limit).all()
    return [TransportIncidentResponse.from_orm(incident) for incident in incidents]


@router.get("/incidents/{incident_id}", response_model=TransportIncidentResponse)
async def get_incident(
    incident_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific transport incident by ID."""
    incident = db.query(TransportIncident).filter(
        and_(TransportIncident.id == incident_id, TransportIncident.tenant_id == tenant_id)
    ).first()
    
    if not incident:
        raise HTTPException(status_code=404, detail="Transport incident not found")
    
    return TransportIncidentResponse.from_orm(incident)


@router.put("/incidents/{incident_id}", response_model=TransportIncidentResponse)
async def update_incident(
    incident_id: str,
    incident: TransportIncidentUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update a transport incident."""
    db_incident = db.query(TransportIncident).filter(
        and_(TransportIncident.id == incident_id, TransportIncident.tenant_id == tenant_id)
    ).first()
    
    if not db_incident:
        raise HTTPException(status_code=404, detail="Transport incident not found")
    
    for field, value in incident.dict(exclude_unset=True).items():
        setattr(db_incident, field, value)
    
    db_incident.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_incident)
    return TransportIncidentResponse.from_orm(db_incident)


# Health Check
@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "transport-service",
        "timestamp": datetime.utcnow().isoformat()
    } 
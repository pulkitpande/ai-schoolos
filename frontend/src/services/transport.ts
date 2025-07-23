import { apiService, ApiResponse } from './api';

// Transport Types
export interface Vehicle {
  id: string;
  vehicleNumber: string;
  vehicleType: 'bus' | 'van' | 'car' | 'minibus';
  capacity: number;
  model: string;
  manufacturer: string;
  year: number;
  color: string;
  registrationNumber: string;
  insuranceNumber: string;
  insuranceExpiry: string;
  fitnessExpiry: string;
  permitExpiry: string;
  driverId?: string;
  conductorId?: string;
  status: 'active' | 'maintenance' | 'inactive';
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface Route {
  id: string;
  name: string;
  description: string;
  startLocation: string;
  endLocation: string;
  distance: number; // in kilometers
  estimatedTime: number; // in minutes
  stops: RouteStop[];
  vehicleId?: string;
  driverId?: string;
  conductorId?: string;
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface RouteStop {
  id: string;
  routeId: string;
  stopName: string;
  stopLocation: string;
  stopOrder: number;
  arrivalTime: string;
  departureTime: string;
  latitude?: number;
  longitude?: number;
  createdAt: string;
  updatedAt: string;
}

export interface TransportBooking {
  id: string;
  studentId: string;
  routeId: string;
  vehicleId?: string;
  pickupLocation: string;
  dropLocation: string;
  pickupTime: string;
  dropTime: string;
  bookingDate: string;
  status: 'confirmed' | 'pending' | 'cancelled' | 'completed';
  fare: number;
  paymentStatus: 'paid' | 'pending' | 'cancelled';
  notes?: string;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface Driver {
  id: string;
  name: string;
  licenseNumber: string;
  licenseType: string;
  licenseExpiry: string;
  phoneNumber: string;
  email?: string;
  address: string;
  experience: number; // in years
  status: 'active' | 'inactive' | 'suspended';
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface Conductor {
  id: string;
  name: string;
  phoneNumber: string;
  email?: string;
  address: string;
  experience: number; // in years
  status: 'active' | 'inactive' | 'suspended';
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface TransportFilters {
  vehicleType?: string;
  routeId?: string;
  driverId?: string;
  status?: string;
  schoolId?: string;
}

export interface TransportListResponse {
  vehicles: Vehicle[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Transport Service class
export class TransportService {
  private readonly TRANSPORT_ENDPOINTS = {
    VEHICLES: '/api/v1/transport/vehicles',
    ROUTES: '/api/v1/transport/routes',
    BOOKINGS: '/api/v1/transport/bookings',
    DRIVERS: '/api/v1/transport/drivers',
    CONDUCTORS: '/api/v1/transport/conductors',
    STOPS: '/api/v1/transport/stops',
    REPORTS: '/api/v1/transport/reports',
  };

  // Get vehicles
  async getVehicles(filters?: TransportFilters): Promise<TransportListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<TransportListResponse>(
      `${this.TRANSPORT_ENDPOINTS.VEHICLES}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch vehicles');
  }

  // Get vehicle by ID
  async getVehicle(id: string): Promise<Vehicle> {
    const response = await apiService.get<Vehicle>(`${this.TRANSPORT_ENDPOINTS.VEHICLES}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch vehicle');
  }

  // Create vehicle
  async createVehicle(data: Partial<Vehicle>): Promise<Vehicle> {
    const response = await apiService.post<Vehicle>(this.TRANSPORT_ENDPOINTS.VEHICLES, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create vehicle');
  }

  // Update vehicle
  async updateVehicle(id: string, data: Partial<Vehicle>): Promise<Vehicle> {
    const response = await apiService.put<Vehicle>(`${this.TRANSPORT_ENDPOINTS.VEHICLES}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update vehicle');
  }

  // Delete vehicle
  async deleteVehicle(id: string): Promise<void> {
    const response = await apiService.delete(`${this.TRANSPORT_ENDPOINTS.VEHICLES}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete vehicle');
    }
  }

  // Get routes
  async getRoutes(filters?: any): Promise<Route[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<Route[]>(
      `${this.TRANSPORT_ENDPOINTS.ROUTES}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch routes');
  }

  // Get route by ID
  async getRoute(id: string): Promise<Route> {
    const response = await apiService.get<Route>(`${this.TRANSPORT_ENDPOINTS.ROUTES}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch route');
  }

  // Create route
  async createRoute(data: Partial<Route>): Promise<Route> {
    const response = await apiService.post<Route>(this.TRANSPORT_ENDPOINTS.ROUTES, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create route');
  }

  // Update route
  async updateRoute(id: string, data: Partial<Route>): Promise<Route> {
    const response = await apiService.put<Route>(`${this.TRANSPORT_ENDPOINTS.ROUTES}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update route');
  }

  // Delete route
  async deleteRoute(id: string): Promise<void> {
    const response = await apiService.delete(`${this.TRANSPORT_ENDPOINTS.ROUTES}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete route');
    }
  }

  // Get route stops
  async getRouteStops(routeId: string): Promise<RouteStop[]> {
    const params = new URLSearchParams();
    params.append('routeId', routeId);

    const response = await apiService.get<RouteStop[]>(
      `${this.TRANSPORT_ENDPOINTS.STOPS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch route stops');
  }

  // Get route stop by ID
  async getRouteStop(id: string): Promise<RouteStop> {
    const response = await apiService.get<RouteStop>(`${this.TRANSPORT_ENDPOINTS.STOPS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch route stop');
  }

  // Create route stop
  async createRouteStop(data: Partial<RouteStop>): Promise<RouteStop> {
    const response = await apiService.post<RouteStop>(this.TRANSPORT_ENDPOINTS.STOPS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create route stop');
  }

  // Update route stop
  async updateRouteStop(id: string, data: Partial<RouteStop>): Promise<RouteStop> {
    const response = await apiService.put<RouteStop>(`${this.TRANSPORT_ENDPOINTS.STOPS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update route stop');
  }

  // Delete route stop
  async deleteRouteStop(id: string): Promise<void> {
    const response = await apiService.delete(`${this.TRANSPORT_ENDPOINTS.STOPS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete route stop');
    }
  }

  // Get transport bookings
  async getTransportBookings(filters?: any): Promise<TransportBooking[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<TransportBooking[]>(
      `${this.TRANSPORT_ENDPOINTS.BOOKINGS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch transport bookings');
  }

  // Get transport booking by ID
  async getTransportBooking(id: string): Promise<TransportBooking> {
    const response = await apiService.get<TransportBooking>(`${this.TRANSPORT_ENDPOINTS.BOOKINGS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch transport booking');
  }

  // Create transport booking
  async createTransportBooking(data: Partial<TransportBooking>): Promise<TransportBooking> {
    const response = await apiService.post<TransportBooking>(this.TRANSPORT_ENDPOINTS.BOOKINGS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create transport booking');
  }

  // Update transport booking
  async updateTransportBooking(id: string, data: Partial<TransportBooking>): Promise<TransportBooking> {
    const response = await apiService.put<TransportBooking>(`${this.TRANSPORT_ENDPOINTS.BOOKINGS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update transport booking');
  }

  // Delete transport booking
  async deleteTransportBooking(id: string): Promise<void> {
    const response = await apiService.delete(`${this.TRANSPORT_ENDPOINTS.BOOKINGS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete transport booking');
    }
  }

  // Get drivers
  async getDrivers(filters?: any): Promise<Driver[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<Driver[]>(
      `${this.TRANSPORT_ENDPOINTS.DRIVERS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch drivers');
  }

  // Get driver by ID
  async getDriver(id: string): Promise<Driver> {
    const response = await apiService.get<Driver>(`${this.TRANSPORT_ENDPOINTS.DRIVERS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch driver');
  }

  // Create driver
  async createDriver(data: Partial<Driver>): Promise<Driver> {
    const response = await apiService.post<Driver>(this.TRANSPORT_ENDPOINTS.DRIVERS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create driver');
  }

  // Update driver
  async updateDriver(id: string, data: Partial<Driver>): Promise<Driver> {
    const response = await apiService.put<Driver>(`${this.TRANSPORT_ENDPOINTS.DRIVERS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update driver');
  }

  // Delete driver
  async deleteDriver(id: string): Promise<void> {
    const response = await apiService.delete(`${this.TRANSPORT_ENDPOINTS.DRIVERS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete driver');
    }
  }

  // Get conductors
  async getConductors(filters?: any): Promise<Conductor[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<Conductor[]>(
      `${this.TRANSPORT_ENDPOINTS.CONDUCTORS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch conductors');
  }

  // Get conductor by ID
  async getConductor(id: string): Promise<Conductor> {
    const response = await apiService.get<Conductor>(`${this.TRANSPORT_ENDPOINTS.CONDUCTORS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch conductor');
  }

  // Create conductor
  async createConductor(data: Partial<Conductor>): Promise<Conductor> {
    const response = await apiService.post<Conductor>(this.TRANSPORT_ENDPOINTS.CONDUCTORS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create conductor');
  }

  // Update conductor
  async updateConductor(id: string, data: Partial<Conductor>): Promise<Conductor> {
    const response = await apiService.put<Conductor>(`${this.TRANSPORT_ENDPOINTS.CONDUCTORS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update conductor');
  }

  // Delete conductor
  async deleteConductor(id: string): Promise<void> {
    const response = await apiService.delete(`${this.TRANSPORT_ENDPOINTS.CONDUCTORS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete conductor');
    }
  }

  // Get student transport bookings
  async getStudentTransportBookings(studentId: string): Promise<TransportBooking[]> {
    const response = await apiService.get<TransportBooking[]>(`${this.TRANSPORT_ENDPOINTS.BOOKINGS}/student/${studentId}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch student transport bookings');
  }

  // Get transport reports
  async getTransportReports(schoolId?: string, dateFrom?: string, dateTo?: string): Promise<any> {
    const params = new URLSearchParams();
    
    if (schoolId) {
      params.append('schoolId', schoolId);
    }
    
    if (dateFrom) {
      params.append('dateFrom', dateFrom);
    }
    
    if (dateTo) {
      params.append('dateTo', dateTo);
    }

    const response = await apiService.get<any>(
      `${this.TRANSPORT_ENDPOINTS.REPORTS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch transport reports');
  }

  // Get transport stats
  async getTransportStats(schoolId?: string): Promise<any> {
    const params = new URLSearchParams();
    
    if (schoolId) {
      params.append('schoolId', schoolId);
    }

    const response = await apiService.get<any>(
      `${this.TRANSPORT_ENDPOINTS.REPORTS}/stats?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch transport stats');
  }
}

// Export singleton instance
export const transportService = new TransportService();
export default transportService; 
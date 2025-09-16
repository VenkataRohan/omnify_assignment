import { Event, Attendee, CreateEventRequest, RegisterAttendeeRequest, ApiResponse, PaginatedResponse } from '@/types/event';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
  private async makeRequest<T>(endpoint: string, options?: RequestInit): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
      }

  const data = await response.json();
  return data;
    } catch (error) {
      console.error(`API Error on ${endpoint}:`, error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'An unknown error occurred',
      };
    }
  }

  // Event endpoints
  async getEvents(): Promise<ApiResponse<Event[]>> {
    return this.makeRequest<Event[]>('/events');
  }

  async getEvent(id: number): Promise<ApiResponse<Event>> {
    return this.makeRequest<Event>(`/events/${id}`);
  }

  async createEvent(event: CreateEventRequest): Promise<ApiResponse<Event>> {
    return this.makeRequest<Event>('/events', {
      method: 'POST',
      body: JSON.stringify(event),
    });
  }

  async updateEvent(id: number, event: Partial<CreateEventRequest>): Promise<ApiResponse<Event>> {
    return this.makeRequest<Event>(`/events/${id}`, {
      method: 'PUT',
      body: JSON.stringify(event),
    });
  }

  async deleteEvent(id: number): Promise<ApiResponse<void>> {
    return this.makeRequest<void>(`/events/${id}`, {
      method: 'DELETE',
    });
  }

  // Attendee endpoints
  async getEventAttendees(eventId: number, page: number = 1, size: number = 10): Promise<PaginatedResponse<Attendee>> {
    return this.makeRequest<any>(`/events/${eventId}/attendees?page=${page}&size=${size}`);
  }

  async registerAttendee(eventId: number, attendee: RegisterAttendeeRequest): Promise<ApiResponse<Attendee>> {
    return this.makeRequest<Attendee>(`/events/${eventId}/attendees`, {
      method: 'POST',
      body: JSON.stringify(attendee),
    });
  }

  async removeAttendee(eventId: number, attendeeId: number): Promise<ApiResponse<void>> {
    return this.makeRequest<void>(`/events/${eventId}/attendees/${attendeeId}`, {
      method: 'DELETE',
    });
  }
}

export const apiService = new ApiService();

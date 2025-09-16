export interface Event {
  id: number;
  name: string;
  location: string;
  start_time: string;
  end_time: string;
  max_capacity: number;
  current_attendees: number;
  created_at: string;
  updated_at: string;
  is_full: boolean;
  available_spots: number;
  capacity_percentage: number;
}

export interface Attendee {
  id: number;
  name: string;
  email: string;
  event_id: number;
  registered_at: string;
}

export interface CreateEventRequest {
  name: string;
  location: string;
  start_time: string;
  end_time: string;
  max_capacity: number;
}

export interface RegisterAttendeeRequest {
  name: string;
  email: string;
}

export interface PaginationMeta {
  page: number;
  size: number;
  total: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface PaginatedResponse<T> {
  success: boolean;
  data?: T[];
  meta?: PaginationMeta;
  message?: string;
  error?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

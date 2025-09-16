"use client";

import { useState, useEffect } from "react";
import { CreateEventForm } from "@/components/CreateEventForm";
import { EventCard } from "@/components/EventCard";
import { TimezoneSelector } from "@/components/TimezoneSelector";
import { TimezoneProvider, useTimezoneContext } from "@/contexts/TimezoneContext";
import { Button } from "@/components/ui/button";
import { Event } from "@/types/event";
import { apiService } from "@/services/api";
import { toast } from "sonner";
import { CalendarDays, RefreshCw, Globe } from "lucide-react";

export default function HomePage() {
  return (
    <TimezoneProvider>
      <EventManagementPage />
    </TimezoneProvider>
  );
}

function EventManagementPage() {
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const { selectedTimezone, setSelectedTimezone } = useTimezoneContext();

  const fetchEvents = async () => {
    if (events.length > 0) {
      setIsRefreshing(true);
    } else {
      setIsLoading(true);
    }
    
    try {
      const response = await apiService.getEvents();
      
      if (response.success && response.data) {
        setEvents(response.data);
      } else {
        toast.error(response.error || "Failed to fetch events");
      }
    } catch (error) {
      toast.error("An unexpected error occurred");
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const handleEventCreated = () => {
    fetchEvents();
  };

  const handleEventUpdated = () => {
    fetchEvents();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading events...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-4">
            <CalendarDays className="h-8 w-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-900">Event Management System</h1>
          </div>
          <p className="text-gray-600 mb-6">
            Create, manage, and track your events with ease. Register attendees and monitor capacity in real-time.
          </p>
          
          {/* Action Bar */}
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
            <div className="flex gap-4 items-center">
              <CreateEventForm onEventCreated={handleEventCreated} />
              <Button
                variant="outline"
                onClick={fetchEvents}
                disabled={isRefreshing}
                className="flex items-center gap-2"
              >
                <RefreshCw className={`h-4 w-4 ${isRefreshing ? "animate-spin" : ""}`} />
                Refresh
              </Button>
            </div>
            
            {/* Timezone Selector */}
            <div className="flex items-center gap-2">
              <Globe className="h-4 w-4 text-gray-600" />
              <span className="text-sm text-gray-600 font-medium">View in:</span>
              <TimezoneSelector
                value={selectedTimezone}
                onValueChange={setSelectedTimezone}
                className="w-[200px]"
                showIcon={false}
              />
            </div>
          </div>
        </div>

        {/* Events Grid */}
        {events.length === 0 ? (
          <div className="text-center py-12">
            <CalendarDays className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No Events Yet</h3>
            <p className="text-gray-600 mb-6">
              Get started by creating your first event. It's quick and easy!
            </p>
            <CreateEventForm onEventCreated={handleEventCreated} />
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {events?.map((event) => (
              <EventCard
                key={event.id}
                event={event}
                onEventUpdated={handleEventUpdated}
              />
            ))}
          </div>
        )}

        {/* Stats Footer */}
        {events.length > 0 && (
          <div className="mt-8 p-6 bg-white rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold mb-4">Overview</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{events.length}</div>
                <div className="text-sm text-gray-600">Total Events</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {events.reduce((sum, event) => sum + event.current_attendees, 0)}
                </div>
                <div className="text-sm text-gray-600">Total Attendees</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {events.filter(event => event.current_attendees >= event.max_capacity).length}
                </div>
                <div className="text-sm text-gray-600">Full Events</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

"use client";

import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Event } from "@/types/event";
import { isEventFull, getCapacityPercentage } from "@/lib/utils";
import { RegisterAttendeeForm } from "./RegisterAttendeeForm";
import { AttendeesModal } from "./AttendeesModal";
import { TimezoneAwareDate } from "./TimezoneAwareDate";
import { useTimezoneContext } from "@/contexts/TimezoneContext";
import { Calendar, Users, Pencil, Trash2 } from "lucide-react";

interface EventCardProps {
  event: Event;
  onEventUpdated: () => void;
  onEditEvent?: (event: Event) => void;
  onDeleteEvent?: (eventId: number) => void;
}

export function EventCard({ event, onEventUpdated, onEditEvent, onDeleteEvent }: EventCardProps) {
  const [showAttendeesModal, setShowAttendeesModal] = useState(false);
  const { selectedTimezone } = useTimezoneContext();
  const capacityPercentage = getCapacityPercentage(event.current_attendees, event.max_capacity);
  const eventFull = isEventFull(event.current_attendees, event.max_capacity);

  const getCapacityBadgeVariant = () => {
    if (eventFull) return "outline";
    if (capacityPercentage > 70) return "outline";
    return "secondary";
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex justify-between items-start gap-1">
          <div>
            <CardTitle className="text-xl mb-2">{event.name}</CardTitle>
            <CardDescription>{event.location}</CardDescription>
          </div>
          <div className="flex items-center">
            <Badge className={`${eventFull ? "bg-red-500" : "bg-green-700"}`}>
              {eventFull ? "Full" : "Available"}
            </Badge>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="flex items-center gap-3 text-sm">
            <Calendar className="h-4 w-4 text-blue-500 flex-shrink-0" />
            <div className="flex items-center gap-3 flex-wrap">
              <div className="flex items-center gap-1">
                <span className="text-xs text-muted-foreground font-medium uppercase tracking-wide">Start:</span>
                <span className="font-medium text-foreground">
                  <TimezoneAwareDate 
                    date={event.start_time} 
                    timezone={selectedTimezone}
                    format="MMM d ''yy '@' h:mm a"
                    showTimezone={false}
                  />
                </span>
              </div>
              <div className="flex items-center gap-1">
                <span className="text-xs text-muted-foreground font-medium uppercase tracking-wide">End:</span>
                <span className="font-medium text-foreground">
                  <TimezoneAwareDate 
                    date={event.end_time} 
                    timezone={selectedTimezone}
                    format="MMM d ''yy '@' h:mm a"
                    showTimezone={true}
                  />
                </span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-3 text-sm">
            <Users className="h-4 w-4 text-green-500 flex-shrink-0" />
            <span className="font-medium text-foreground">
              {event.current_attendees} / {event.max_capacity} attendees
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-300 ${
                eventFull 
                  ? "bg-red-500" 
                  : capacityPercentage > 70 
                  ? "bg-yellow-500" 
                  : "bg-green-500"
              }`}
              style={{ width: `${Math.min(capacityPercentage, 100)}%` }}
            />
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex justify-between flex-wrap">
        <RegisterAttendeeForm
          eventId={event.id}
          isEventFull={eventFull}
          onAttendeeRegistered={onEventUpdated}
        />
        <Button
          variant="outline"
          onClick={() => setShowAttendeesModal(true)}
          className="flex items-center gap-2"
        >
          <Users className="h-4 w-4" />
          View Attendees
          {event.current_attendees > 0 && (
            <Badge variant="secondary" className="ml-1">
              {event.current_attendees}
            </Badge>
          )}
        </Button>
      </CardFooter>
      
      <AttendeesModal
        isOpen={showAttendeesModal}
        onClose={() => setShowAttendeesModal(false)}
        eventId={event.id}
        eventName={event.name}
        onAttendeeRemoved={onEventUpdated}
      />
    </Card>
  );
}

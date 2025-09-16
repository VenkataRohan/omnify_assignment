"use client";

import { useState, useEffect, useCallback } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Attendee } from "@/types/event";
import { apiService } from "@/services/api";
import { toast } from "sonner";
import { formatDate } from "@/lib/utils";
import { Trash2, Users, Loader2 } from "lucide-react";
import { useInfiniteScroll } from "@/hooks/useInfiniteScroll";

interface AttendeesListProps {
  eventId: number;
  onAttendeeRemoved: () => void;
}

export function AttendeesList({ eventId, onAttendeeRemoved }: AttendeesListProps) {
  const [attendees, setAttendees] = useState<Attendee[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasNextPage, setHasNextPage] = useState(false);
  const [totalAttendees, setTotalAttendees] = useState(0);
  const pageSize = 2; // Match your backend page size

  const fetchAttendees = useCallback(async (page: number = 1, reset: boolean = true) => {
    if (page === 1) {
      setIsLoading(true);
    } else {
      setIsLoadingMore(true);
    }

    try {
      const response = await apiService.getEventAttendees(eventId, page, pageSize);
      if (response.success && response.data && response.meta) {
        if (reset) {
          setAttendees(response.data);
        } else {
          setAttendees(prev => [...prev, ...response.data!]);
        }
        
        setHasNextPage(response.meta.has_next);
        setTotalAttendees(response.meta.total);
        setCurrentPage(page);
      } else {
        toast.error(response.error || "Failed to fetch attendees");
      }
    } catch (error) {
      toast.error("An unexpected error occurred");
    } finally {
      setIsLoading(false);
      setIsLoadingMore(false);
    }
  }, [eventId, pageSize]);

  const loadMoreAttendees = useCallback(() => {
    if (!isLoadingMore && hasNextPage) {
      fetchAttendees(currentPage + 1, false);
    }
  }, [currentPage, hasNextPage, isLoadingMore, fetchAttendees]);

  const { containerRef } = useInfiniteScroll({
    hasNextPage,
    isLoading: isLoadingMore,
    onLoadMore: loadMoreAttendees,
    threshold: 50  // Smaller threshold for better responsiveness
  });



  useEffect(() => {
    fetchAttendees(1, true);
  }, [eventId]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="text-sm text-muted-foreground">Loading attendees...</div>
      </div>
    );
  }

  if (attendees.length === 0 && !isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-8 text-center">
        <Users className="h-12 w-12 text-muted-foreground mb-4" />
        <div className="text-sm text-muted-foreground">No attendees registered yet</div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Users className="h-4 w-4" />
        <span className="text-sm font-medium">Registered Attendees</span>
        <Badge variant="secondary">{totalAttendees}</Badge>
      </div>
      
      <div 
        ref={containerRef}
        className="border rounded-lg h-64 overflow-y-auto"
      >
        <div className="p-2 text-xs text-gray-500 border-b">
          Page {currentPage} | Total: {totalAttendees} | Has Next: {hasNextPage ? 'Yes' : 'No'}
        </div>
        <Table>
          <TableHeader className="sticky top-0 bg-white">
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {attendees.map((attendee) => (
              <TableRow key={attendee.id}>
                <TableCell className="font-medium py-4">{attendee.name}</TableCell>
                <TableCell className="py-4">{attendee.email}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        
        {isLoadingMore && (
          <div className="flex items-center justify-center py-4 border-t">
            <Loader2 className="h-4 w-4 animate-spin mr-2" />
            <span className="text-sm text-muted-foreground">Loading more attendees...</span>
          </div>
        )}
        
        {!hasNextPage && attendees.length > 0 && !isLoadingMore && (
          <div className="flex items-center justify-center py-4 border-t">
            <span className="text-sm text-muted-foreground">All attendees loaded</span>
          </div>
        )}
        
        {/* Add minimum content to ensure scrolling */}
        <div className="h-32 flex items-center justify-center text-gray-400 text-sm">
          {hasNextPage ? "Scroll down to load more attendees" : ""}
        </div>
      </div>
    </div>
  );
}

"use client";

import { useState, useEffect, useCallback } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Attendee } from "@/types/event";
import { apiService } from "@/services/api";
import { toast } from "sonner";
import { Users, Loader2 } from "lucide-react";
import { useInfiniteScroll } from "@/hooks/useInfiniteScroll";

interface AttendeesModalProps {
  isOpen: boolean;
  onClose: () => void;
  eventId: number;
  eventName: string;
  onAttendeeRemoved: () => void;
}

export function AttendeesModal({ 
  isOpen, 
  onClose, 
  eventId, 
  eventName, 
  onAttendeeRemoved 
}: AttendeesModalProps) {
  const [attendees, setAttendees] = useState<Attendee[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasNextPage, setHasNextPage] = useState(false);
  const [totalAttendees, setTotalAttendees] = useState(0);
  const pageSize = 10;

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
    threshold: 100  // Load more when 100px from bottom
  });

  // Reset state when modal opens/closes or eventId changes
  useEffect(() => {
    if (isOpen) {
      setAttendees([]);
      setCurrentPage(1);
      setHasNextPage(false);
      setTotalAttendees(0);
      fetchAttendees(1, true);
    }
  }, [isOpen, eventId, fetchAttendees]);

  if (!isOpen) return null;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[70vh] flex flex-col">
        <DialogHeader className="border-b pb-4">
          <DialogTitle className="flex items-center gap-3 text-xl">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
            <div className="flex-1">
              <div className="font-semibold">{eventName}</div>
              <div className="text-sm font-normal text-muted-foreground mt-1">
                Showing {attendees.length} of {totalAttendees} attendees
              </div>
            </div>
          </DialogTitle>
        </DialogHeader>
        
        <div className="flex-1 overflow-hidden mt-4">
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-blue-600 mb-4" />
              <div className="text-muted-foreground">Loading attendees...</div>
            </div>
          ) : attendees.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="p-4 bg-gray-100 rounded-full mb-4">
                <Users className="h-12 w-12 text-gray-400" />
              </div>
              <div className="text-lg font-medium text-gray-900 mb-2">No attendees yet</div>
              <div className="text-muted-foreground">Be the first to register for this event!</div>
            </div>
          ) : (
            <div 
              ref={containerRef}
              className="border rounded-xl bg-white shadow-sm overflow-y-auto"
              style={{ 
                height: '400px', // Fixed height to ensure scrolling
                scrollbarWidth: 'thin',
                scrollbarColor: '#CBD5E0 #F7FAFC'
              }}
            >
              <Table>
                <TableHeader className="sticky top-0 bg-white z-10 border-b">
                  <TableRow className="hover:bg-transparent">
                    <TableHead className="py-4 font-semibold text-gray-900">Name</TableHead>
                    <TableHead className="py-4 font-semibold text-gray-900">Email</TableHead>
                    <TableHead className="py-4 font-semibold text-gray-900">Registered</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {attendees.map((attendee, index) => (
                    <TableRow 
                      key={attendee.id} 
                      className="hover:bg-gray-50 transition-colors"
                    >
                      <TableCell className="py-4">
                        <span className="font-medium text-gray-900">{attendee.name}</span>
                      </TableCell>
                      <TableCell className="py-4 text-gray-600">{attendee.email}</TableCell>
                      <TableCell className="py-4 text-sm text-gray-500">
                        {new Date(attendee.registered_at).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              
              {isLoadingMore && (
                <div className="flex items-center justify-center py-6 border-t bg-gray-50">
                  <Loader2 className="h-5 w-5 animate-spin text-blue-600 mr-3" />
                  <span className="text-sm text-gray-600">Loading more attendees...</span>
                </div>
              )}
              
              {!hasNextPage && attendees.length > 0 && !isLoadingMore && (
                <div className="flex items-center justify-center py-6 border-t bg-gray-50">
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span>All attendees loaded</span>
                  </div>
                </div>
              )}
              
              {/* Scroll hint for more content - more visible */}
              {hasNextPage && !isLoadingMore && attendees.length >= pageSize && (
                <div className="flex items-center justify-center py-6 border-t-2 border-blue-200 bg-gradient-to-b from-blue-50 to-blue-100">
                  <div className="flex flex-col items-center gap-2 text-blue-700">
                    <div className="animate-bounce text-xl">⬇️</div>
                    <span className="font-medium">Scroll down to load more attendees</span>
                    <span className="text-xs text-blue-600">({totalAttendees - attendees.length} more available)</span>
                  </div>
                </div>
              )}
              
              {/* Spacer to ensure scroll works properly */}
              <div className="h-4"></div>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
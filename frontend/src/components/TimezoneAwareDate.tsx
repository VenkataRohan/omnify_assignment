"use client";

import { TimezoneHelper } from "@/lib/timezone";

interface TimezoneAwareDateProps {
  date: string;
  timezone?: string;
  format?: string;
  showTimezone?: boolean;
  className?: string;
}

export function TimezoneAwareDate({ 
  date, 
  timezone, 
  format = "PPP 'at' p",
  showTimezone = true,
  className = ""
}: TimezoneAwareDateProps) {
  const userTimezone = timezone || TimezoneHelper.getUserTimezone();
  
  try {
    // Pass the string date directly to ensure it's treated as UTC
    const formattedDate = TimezoneHelper.formatDateInTimezone(date, userTimezone, format);
    const timezoneOffset = TimezoneHelper.getTimezoneOffset(userTimezone);
    
    return (
      <span 
        className={className}
        title={`${formattedDate} ${showTimezone ? `(${userTimezone})` : ''}`}
      >
        {formattedDate}
        {showTimezone && (
          <span className="text-muted-foreground ml-1">
            {timezoneOffset}
          </span>
        )}
      </span>
    );
  } catch (error) {
    // Silently handle date formatting errors
    return (
      <span className={`text-red-500 ${className}`}>
        Invalid date
      </span>
    );
  }
}

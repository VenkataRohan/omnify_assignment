"use client";

import { useState, useEffect, useMemo } from 'react';
import { TimezoneHelper } from '@/lib/timezone';

export interface TimezoneInfo {
  value: string;
  label: string;
  offset: string;
}

export function useTimezone() {
  const [userTimezone, setUserTimezone] = useState<string>('UTC');
  const [isLoading, setIsLoading] = useState(true);

  const commonTimezones: TimezoneInfo[] = useMemo(() => [
    { value: 'America/New_York', label: 'Eastern Time (ET)', offset: 'UTC-5/-4' },
    { value: 'America/Chicago', label: 'Central Time (CT)', offset: 'UTC-6/-5' },
    { value: 'America/Denver', label: 'Mountain Time (MT)', offset: 'UTC-7/-6' },
    { value: 'America/Los_Angeles', label: 'Pacific Time (PT)', offset: 'UTC-8/-7' },
    { value: 'Europe/London', label: 'London (GMT)', offset: 'UTC+0/+1' },
    { value: 'Europe/Paris', label: 'Paris (CET)', offset: 'UTC+1/+2' },
    { value: 'Europe/Berlin', label: 'Berlin (CET)', offset: 'UTC+1/+2' },
    { value: 'Asia/Tokyo', label: 'Tokyo (JST)', offset: 'UTC+9' },
    { value: 'Asia/Shanghai', label: 'Shanghai (CST)', offset: 'UTC+8' },
    { value: 'Asia/Kolkata', label: 'India (IST)', offset: 'UTC+5:30' },
    { value: 'Australia/Sydney', label: 'Sydney (AEDT)', offset: 'UTC+10/+11' },
    { value: 'UTC', label: 'UTC', offset: 'UTC+0' },
  ], []);

  useEffect(() => {
    try {
      const timezone = TimezoneHelper.getUserTimezone();
      setUserTimezone(timezone);
    } catch (error) {
      console.warn('Failed to detect user timezone, falling back to UTC');
      setUserTimezone('UTC');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const formatDate = (date: string | Date, timezone?: string, format?: string) => {
    return TimezoneHelper.formatDateInTimezone(
      date, 
      timezone || userTimezone, 
      format
    );
  };

  const convertToUTC = (date: Date, fromTimezone?: string) => {
    return TimezoneHelper.convertToUTC(date, fromTimezone || userTimezone);
  };

  const getCommonTimezones = () => {
    return TimezoneHelper.getCommonTimezones();
  };

  return {
    userTimezone,
    isLoading,
    commonTimezones,
    formatDate,
    convertToUTC,
    getCommonTimezones,
    setUserTimezone,
    getTimezoneDisplayName: TimezoneHelper.getTimezoneDisplayName,
    getTimezoneOffset: TimezoneHelper.getTimezoneOffset,
    isValidTimezone: TimezoneHelper.isValidTimezone,
  };
}

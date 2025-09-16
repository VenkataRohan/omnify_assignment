import { format, parseISO } from 'date-fns';
import { formatInTimeZone, toZonedTime } from 'date-fns-tz';

export class TimezoneHelper {
  /**
   * Get the user's current timezone
   */
  static getUserTimezone(): string {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
  }

  /**
   * Convert a date to UTC for storage
   */
static convertToUTC(date: Date, fromTimezone?: string): string {
    if (fromTimezone) {
        // Convert the date from the given timezone to UTC
        const zonedDate = toZonedTime(date, fromTimezone);
        // Get the equivalent UTC date
        const utcDate = new Date(zonedDate.getTime() - zonedDate.getTimezoneOffset() * 60000);
        console.log(date);
        console.log(zonedDate);
        console.log(utcDate);
        
        return utcDate.toISOString();
    }
    // If no timezone is provided, assume date is in local time
    return date.toISOString();
}

  /**
   * Format a date in a specific timezone
   */
  static formatDateInTimezone(
    date: Date | string, 
    timezone: string, 
    formatString: string = 'PPP p'
  ): string {
    // Ensure the date is treated as UTC
    const dateObj = typeof date === 'string' ? parseISO(date + 'Z') : new Date(date.getTime());
    console.log(dateObj);
    console.log(timezone);
    console.log(formatString);
    console.log(formatInTimeZone(dateObj, timezone, formatString));
    return formatInTimeZone(dateObj, timezone, formatString);
  }

  /**
   * Get timezone offset for display
   */
  static getTimezoneOffset(timezone: string): string {
    const now = new Date();
    const formatter = new Intl.DateTimeFormat('en', {
      timeZone: timezone,
      timeZoneName: 'short'
    });
    const parts = formatter.formatToParts(now);
    return parts.find(part => part.type === 'timeZoneName')?.value || '';
  }

  /**
   * Get a formatted timezone display name
   */
  static getTimezoneDisplayName(timezone: string): string {
    const offset = this.getTimezoneOffset(timezone);
    const cityName = timezone.split('/').pop()?.replace('_', ' ');
    return `${cityName} (${offset})`;
  }

  /**
   * Common timezones for selection
   */
  static getCommonTimezones() {
    return [
      { value: 'America/New_York', label: 'Eastern Time (ET)' },
      { value: 'America/Chicago', label: 'Central Time (CT)' },
      { value: 'America/Denver', label: 'Mountain Time (MT)' },
      { value: 'America/Los_Angeles', label: 'Pacific Time (PT)' },
      { value: 'Europe/London', label: 'London (GMT)' },
      { value: 'Europe/Paris', label: 'Paris (CET)' },
      { value: 'Europe/Berlin', label: 'Berlin (CET)' },
      { value: 'Asia/Tokyo', label: 'Tokyo (JST)' },
      { value: 'Asia/Kolkata', label: 'India (IST)' },
      { value: 'Asia/Shanghai', label: 'Shanghai (CST)' },
      { value: 'Australia/Sydney', label: 'Sydney (AEST)' },
      { value: 'UTC', label: 'UTC' },
    ];
  }

  /**
   * Validate if a timezone string is valid
   */
  static isValidTimezone(timezone: string): boolean {
    try {
      Intl.DateTimeFormat(undefined, { timeZone: timezone });
      return true;
    } catch {
      return false;
    }
  }
}

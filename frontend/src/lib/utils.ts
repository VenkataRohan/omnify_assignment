import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function formatDateForInput(dateString: string): string {
  const date = new Date(dateString);
  return date.toISOString().slice(0, 16);
}

export function isEventFull(currentAttendees: number, maxCapacity: number): boolean {
  return currentAttendees >= maxCapacity;
}

export function getCapacityPercentage(currentAttendees: number, maxCapacity: number): number {
  return (currentAttendees / maxCapacity) * 100;
}

"use client";

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { useTimezone } from '@/hooks/useTimezone';

interface TimezoneContextType {
  selectedTimezone: string;
  setSelectedTimezone: (timezone: string) => void;
  userTimezone: string;
}

const TimezoneContext = createContext<TimezoneContextType | undefined>(undefined);

interface TimezoneProviderProps {
  children: ReactNode;
}

export function TimezoneProvider({ children }: TimezoneProviderProps) {
  const { userTimezone } = useTimezone();
  const [selectedTimezone, setSelectedTimezone] = useState(userTimezone);

  // Update selectedTimezone when userTimezone is detected
  React.useEffect(() => {
    if (userTimezone) {
      setSelectedTimezone(userTimezone);
    }
  }, [userTimezone]);

  return (
    <TimezoneContext.Provider
      value={{
        selectedTimezone,
        setSelectedTimezone,
        userTimezone,
      }}
    >
      {children}
    </TimezoneContext.Provider>
  );
}

export function useTimezoneContext() {
  const context = useContext(TimezoneContext);
  if (context === undefined) {
    throw new Error('useTimezoneContext must be used within a TimezoneProvider');
  }
  return context;
}

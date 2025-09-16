"use client";

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Globe } from "lucide-react";
import { useTimezone } from "@/hooks/useTimezone";

interface TimezoneSelectorProps {
  value?: string;
  onValueChange: (timezone: string) => void;
  placeholder?: string;
  showIcon?: boolean;
  className?: string;
}

export function TimezoneSelector({ 
  value, 
  onValueChange, 
  placeholder = "Select timezone",
  showIcon = true,
  className = ""
}: TimezoneSelectorProps) {
  const { userTimezone, commonTimezones } = useTimezone();

  const getCurrentTimezoneLabel = () => {
    const current = commonTimezones.find(tz => tz.value === (value || userTimezone));
    return current?.label || value || userTimezone;
  };

  return (
    <Select value={value || userTimezone} onValueChange={onValueChange}>
      <SelectTrigger className={className}>
        <div className="flex items-center space-x-2">
          {showIcon && <Globe className="h-4 w-4" />}
          <SelectValue placeholder={placeholder}>
            {getCurrentTimezoneLabel()}
          </SelectValue>
        </div>
      </SelectTrigger>
      <SelectContent>
        <SelectItem value={userTimezone}>
          <div className="flex flex-col">
            <span>🏠 Your Timezone</span>
            <span className="text-xs text-muted-foreground">
              {commonTimezones.find(tz => tz.value === userTimezone)?.label || userTimezone}
            </span>
          </div>
        </SelectItem>
        <div className="border-t my-1" />
        {commonTimezones.map((tz) => (
          <SelectItem key={tz.value} value={tz.value}>
            <div className="flex justify-between items-center w-full">
              <span>{tz.label}</span>
              <span className="text-xs text-muted-foreground ml-2">
                {tz.offset}
              </span>
            </div>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}

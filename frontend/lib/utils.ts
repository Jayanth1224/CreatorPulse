import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: Date | string | null | undefined): string {
  if (!date) return "N/A";
  
  const d = typeof date === "string" ? new Date(date) : date;
  
  // Check if date is invalid
  if (isNaN(d.getTime())) return "Invalid date";
  
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function formatTime(date: Date | string | null | undefined): string {
  if (!date) return "N/A";
  
  const d = typeof date === "string" ? new Date(date) : date;
  
  // Check if date is invalid
  if (isNaN(d.getTime())) return "Invalid time";
  
  return d.toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
  });
}

export function formatDateTime(date: Date | string | null | undefined): string {
  if (!date) return "N/A";
  return `${formatDate(date)} at ${formatTime(date)}`;
}


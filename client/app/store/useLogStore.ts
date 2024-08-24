"use client"

import { create } from "zustand";
import { useEffect } from "react";

interface LogEntry {
  message: string;
  type: string;
  timestamp: string;
}

interface LogStore {
  logs: LogEntry[];
  addLog: (message: string, type: string) => void;
  clearLogs: () => void;
}

const useLogStore = create<LogStore>((set) => ({
  logs: [
    {
      message: "Console up and running. Welcome to the bellmanBot v1",
      type: "log",
      timestamp: "Good day!", // Placeholder during SSR
    },
  ],

  addLog: (message, type) =>
    set((state) => ({
      logs: [
        ...state.logs,
        {
          message,
          type,
          timestamp: new Date().toLocaleTimeString(),
        },
      ],
    })),

  clearLogs: () => set({ logs: [] }),
}));

// Custom hook to update the initial log timestamp after hydration
export const useInitializeLogs = () => {
  const updateLogTimestamp = useLogStore((state) => state.addLog);
  
  useEffect(() => {
    updateLogTimestamp("Console initialized", "log");
  }, []);
};

export default useLogStore;
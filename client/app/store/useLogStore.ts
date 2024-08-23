import { create } from "zustand";

interface LogEntry {
  message: string;
  type: string;
  timestamp: string; // Change to string for time representation
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
      timestamp: new Date().toLocaleTimeString(), // Initialize with current time
    },
  ],

  // Add a log entry
  addLog: (message, type) =>
    set((state) => ({
      logs: [
        ...state.logs,
        {
          message,
          type,
          timestamp: new Date().toLocaleTimeString(), // Include only time
        },
      ],
    })),

  // Clear all log entries
  clearLogs: () => set({ logs: [] }),
}));

export default useLogStore;
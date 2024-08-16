import { createStore } from "zustand";
import { create } from "zustand/vanilla";
import { useStore } from "zustand/react";

interface LogEntry {
  message: string;
  type: "log" | "warn" | "error";
}

interface LogStore {
  logs: LogEntry[];
  addLog: (message: string, type?: "log" | "warn" | "error") => void;
  clearLogs: () => void;
}

// Create the vanilla store
const logStore = createStore<LogStore>((set) => ({
  logs: [{ message: "welcome to the BellmanBot!", type: "log" }],
  addLog: (message, type = "log") =>
    set((state) => ({
      logs: [...state.logs, { message, type }],
    })),
  clearLogs: () => set({ logs: [] }),
}));

// Create the hook for using the store
const useLogStore = () => useStore(logStore);

export default useLogStore;

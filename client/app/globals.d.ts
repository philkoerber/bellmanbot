interface Window {
  ourConsole?: {
    log: (message: string, type?: "log" | "warn" | "error") => void;
  };
}

"use client";

import { useState } from "react";
import Button from "./Button";

interface LogEntry {
  message: string;
  type: "log" | "warn" | "error";
}

const OurConsole = () => {
  const [logs, setLogs] = useState<LogEntry[]>([
    { message: "welcome to the BellmanBot!", type: "log" },
  ]);

  const log = (message: string, type: LogEntry["type"] = "log") => {
    setLogs((prevLogs) => [...prevLogs, { message, type }]);
  };

  // Expose the log function globally for ease of use
  (window as any).customConsole = { log };

  return (
    <div className="top-0 left-0 w-full p-2  text-pakistan overflow-y-auto z-50">
      <div className="flex justify-between">
        <h2 className="text-xl">console</h2>
        <Button onClick={() => setLogs([])} text="Clear" variant="secondary" />
      </div>
      <ul className="mt-2">
        {logs.map((log, index) => (
          <li
            key={index}
            className={
              log.type === "log"
                ? "text-pakistan"
                : log.type === "warn"
                ? "text-yellow-400"
                : "text-red-400"
            }>
            [{log.type.toUpperCase()}] {log.message}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OurConsole;

"use client";

import { useEffect, useRef } from "react";
import Button from "./Button";
import useLogStore from "../store/useLogStore"; 

const OurConsole = () => {
  const addLog = useLogStore((state) => state.addLog);
  const logs = useLogStore((state) => state.logs);
  const clearLogs = useLogStore((state) => state.clearLogs);
  const hasFetched = useRef(false);

  const fetchHealthStatus = async () => {
    addLog("Fetching health status...", "log");
    try {
      const response = await fetch("/api/health_status", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const result = await response.json();
      addLog(`Health Status: ${result.message}`, "log");
    } catch (error) {
      addLog("Error calling /api/health_status... Probably the server is down.", "error");
    }
  };

  useEffect(() => {
    if (hasFetched.current) return;
    fetchHealthStatus();
    hasFetched.current = true; // Mark as fetched
  }, []);

  return (
    <div className="top-0 left-0 w-full p-2 text-pakistan overflow-y-auto z-50">
      <div className="flex justify-between items-center absolute gap-2">
        <Button onClick={fetchHealthStatus} text="Health Status" variant="secondary" />
        <Button onClick={clearLogs} text="Clear" variant="secondary" />
      </div>
      <ul className="mt-12">
        {logs.map((log, index) => (
          <li
            key={index}
            className={
              log.type === "log"
                ? "text-pakistan"
                : log.type === "warn"
                ? "text-yellow-400"
                : "text-red-400"
            }
          >
            <p className="font-extralight inline">
              {log.timestamp} {/* Display only the time */}
            </p>
            <p className="inline ml-2">{log.message}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OurConsole;

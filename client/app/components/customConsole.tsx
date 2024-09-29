"use client";

import { useEffect } from "react";
import Button from "./Button";
import useLogStore from "../store/useLogStore"; 
import useSocketStore from "../store/socketStore"; // Import the socket store

const OurConsole = () => {
  const addLog = useLogStore((state) => state.addLog);
  const logs = useLogStore((state) => state.logs);
  const clearLogs = useLogStore((state) => state.clearLogs);
  const { triggerTestButton } = useSocketStore(); // Get the function from the socket store

  const handleTestButtonClick = () => {
    triggerTestButton(); // Call the function to trigger the event
    addLog('Clicked Test button', "log"); // Log the button click
  };

  return (
    <div className="top-0 left-0 w-full p-2 text-pakistan overflow-y-auto z-50">
      <div className="flex justify-between items-center absolute gap-2">
        <Button onClick={clearLogs} variant="secondary">Clear</Button>
        <Button onClick={handleTestButtonClick} variant="primary">Test Button</Button>
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
              {log.timestamp}
            </p>
            <p className="inline ml-2">{log.message}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OurConsole;

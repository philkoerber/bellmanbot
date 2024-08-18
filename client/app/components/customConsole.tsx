"use client";

import Button from "./Button";
import useLogStore from "./useLogStore"; // Import the Zustand store

const OurConsole = () => {
  // Access the Zustand store state and actions
  const logs = useLogStore((state) => state.logs);
  const clearLogs = useLogStore((state) => state.clearLogs);

  return (
    <div className="top-0 left-0 w-full p-2 text-pakistan overflow-y-auto z-50">
      <div className="flex justify-between items-center absolute">
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
            }>
            [{log.type.toUpperCase()}] {log.message}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OurConsole;

"use client";

import Button from "./Button";
import useLogStore from "../store/logStore"; 

const OurConsole = () => {
  const logs = useLogStore((state) => state.logs);
  const clearLogs = useLogStore((state) => state.clearLogs);


  return (
    <div className="top-0 left-0 w-full p-2 text-pakistan overflow-y-auto z-50">
      <div className="flex justify-between items-center absolute gap-2">
        <Button onClick={clearLogs} variant="secondary">Clear</Button>
      </div>
      <ul className="mt-12">
        {logs.map((log, index) => (
          <li
            key={index}
            className={
              log.type === "log"
                ? "text-pakistan"
                : log.type === "warning"
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

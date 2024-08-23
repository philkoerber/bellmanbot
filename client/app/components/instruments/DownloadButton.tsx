// DownloadButton.js

import React from 'react';
import Button from '../Button'; // Adjust the import path according to your file structure
import useLogStore from "@/app/store/useLogStore";
import { InstrumentProps } from './types';

const DownloadButton :React.FC<InstrumentProps> = ({ symbol }) => {
  // Extract addLog from the useLogStore hook
  const addLog = useLogStore((state) => state.addLog);

  // Define the function to handle the download button click
  const handleDownloadButton = () => {
    addLog(`Starting download for instrument ${symbol}`, "log");
    const eventSource = new EventSource(`/api/download?symbol=${symbol}`);
  
    eventSource.onmessage = (event) => {
      addLog(event.data, "log");
  
      if (event.data.includes("Download complete")) {
        eventSource.close();
      }
    };
  
    eventSource.onerror = (error) => {
      addLog("Error in downloading data", "error");
      console.error("SSE error:", error);
      eventSource.close();
    };
  };

  return (
    <Button
      text="Download"
      variant="primary"
      onClick={handleDownloadButton} // Bind handleDownloadButton to the button click
    />
  );
};

export default DownloadButton;

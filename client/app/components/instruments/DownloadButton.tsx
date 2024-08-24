"use client"

import React from 'react';
import Button from '../Button'; // Adjust the import path according to your file structure
import useLogStore from "@/app/store/useLogStore";
import useMetadataStore from "@/app/store/useMetadataStore"; // Import the metadata store
import { InstrumentProps } from './types';

const DownloadButton: React.FC<InstrumentProps> = ({ symbol }) => {
  // Extract addLog from the useLogStore hook
  const addLog = useLogStore((state) => state.addLog);

  // Extract the metadata for the given symbol from useMetadataStore
  const lastDownloadedAt = useMetadataStore(
    (state) => state.downloadedInstruments[symbol]?.lastDownloadedAt
  );

  console.log(lastDownloadedAt)

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
    <>
      <Button
        text="Download"
        variant="primary"
        onClick={handleDownloadButton} // Bind handleDownloadButton to the button click
      />
      <p className="text-[10px] text-sage -mt-1">
      {lastDownloadedAt ? (
        <>Last downloaded: {lastDownloadedAt}</>
      ) : (
        <>No data available</>
      )}
      </p>
    </>
  );
};

export default DownloadButton;

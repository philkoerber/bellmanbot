"use client";

import React from 'react';
import Button from '../Button'; // Adjust the import path according to your file structure
import { InstrumentProps } from '@/app/globals';

interface DownloadButtonProps extends InstrumentProps {
  lastModified: string;
  loading: boolean;
  setLoading: (loading: boolean) => void;
  fetchDownloadedMetadata: () => Promise<void>;
  addLog: (message: string, type: string) => void;
}

const DownloadButton: React.FC<DownloadButtonProps> = ({
  symbol,
  lastModified,
  loading,
  setLoading,
  fetchDownloadedMetadata,
  addLog,
}) => {

  const handleDownloadButton = () => {
    addLog(`Starting download for instrument ${symbol}`, "log");
    setLoading(true); // Disable button while downloading

    const eventSource = new EventSource(`/api/download?symbol=${symbol}`);

    eventSource.onmessage = (event) => {
      addLog(event.data, "log");

      if (event.data.includes("Download complete")) {
        eventSource.close();
        fetchDownloadedMetadata(); // Fetch metadata again after download completes
        setLoading(false); // Re-enable button after completion
      }
    };

    eventSource.onerror = (error) => {
      addLog("Error in downloading data", "error");
      console.error("SSE error:", error);
      eventSource.close();
      setLoading(false); // Re-enable button on error
    };
  };

  return (
    <>
      <Button
        text="Download"
        variant="primary"
        onClick={handleDownloadButton}
        disabled={loading} // Disable the button when loading
      />
      <p className="text-[10px] text-sage -mt-1 h-7">
        {lastModified}
      </p>
    </>
  );
};

export default DownloadButton;

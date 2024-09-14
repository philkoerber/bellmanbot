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

  const handleDownloadButton = async () => {
    addLog(`Starting download for instrument ${symbol}`, "log");
    setLoading(true); // Disable button while downloading

    try {
      const response = await fetch(`/api/download?symbol=${symbol}`, { method: 'POST' });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      if (data.job_id) {
        addLog(`Download started with job ID ${data.job_id}`, "log");
        
        // Optionally, you can implement a polling mechanism to check the status of the job periodically
        // until it completes. This will help to keep an eye on the job progress.
        
        setLoading(false); // Re-enable button after initiating the download process
      } else {
        throw new Error('No job ID received');
      }

    } catch (error) {
      addLog(`Error in downloading data: ${error}`, "error");
      console.error("Fetch error:", error);
    } finally {
      setLoading(false); // Re-enable button on error or after process completion
    }
  };

  return (
    <div>
      <Button
        text="Download"
        variant="primary"
        onClick={handleDownloadButton}
        disabled={loading} // Disable the button when loading
      />
      <p className="text-[10px] text-sage mt-1 h-7">
        {lastModified}
      </p>
    </div>
  );
};

export default DownloadButton;
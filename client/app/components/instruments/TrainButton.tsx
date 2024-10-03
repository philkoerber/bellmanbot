"use client";

import React, { useState, useEffect } from 'react';
import Button from '../Button'; // Adjust the import path according to your file structure
import useLogStore from "@/app/store/logStore";
import { InstrumentProps } from '@/app/globals';

const TrainButton: React.FC<InstrumentProps> = ({ symbol }) => {
  // State to manage the loading state of the button
  const [loading, setLoading] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [results, setResults] = useState<any>(null); // Adjust type according to the results structure
  const [intervalId, setIntervalId] = useState<NodeJS.Timeout | null>(null);

  // Extract addLog from the useLogStore hook
  const addLog = useLogStore((state) => state.addLog);

  // Define the function to handle the train button click
  const handleTrainButton = async () => {
    addLog(`Starting training a model for ${symbol}`, "log");
    setLoading(true); // Disable the button when clicked

    try {
      const response = await fetch(`/api/train?symbol=${symbol}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const result = await response.json();
      addLog(`Train API Response: ${result.message}`, "log");

      // Assuming the response contains a job ID
      if (result.job_id) {
        setJobId(result.job_id);
        // Start polling for job status
        const id = setInterval(async () => {
          await pollJobStatus(result.job_id);
        }, 5000); // Poll every 5 seconds
        setIntervalId(id);
      } else {
        addLog("Training job ID not received", "error");
      }
    } catch (error) {
      console.error("Error calling /api/train:", error);
      addLog("Error calling /api/train", "error");
    } finally {
      setLoading(false); // Re-enable the button once the API call is complete
    }
  };

  // Polling function to check job status
  const pollJobStatus = async (jobId: string) => {
    try {
      const response = await fetch(`/api/job_status?job_id=${jobId}`);
      
      if (!response.ok) throw new Error(`Error: ${response.statusText}`);
      const data = await response.json();
      console.log(data);
      setStatus(data.status);

      if (data.status === 'SUCCESS') {
        clearInterval(intervalId as NodeJS.Timeout);
        setIntervalId(null);
        await fetchResults(jobId);
      } else if (data.status === 'PENDING') {
        // Continue polling if status is 'pending'
        return;
      } else {
        // Handle unexpected status
        clearInterval(intervalId as NodeJS.Timeout);
        setIntervalId(null);
        addLog(`Job status is ${data.status}, which is unexpected`, "error");
      }
    } catch (error) {
      console.error("Error polling job status:", error);
      addLog("Error polling job status", "error");
    }
  };

  // Function to fetch training results
  const fetchResults = async (jobId: string) => {
    try {
      const response = await fetch(`/api/results?symbol=${symbol}`);
      if (!response.ok) throw new Error(`Error: ${response.statusText}`);
      const data = await response.json();
      setResults(data);
      addLog("Training results fetched successfully", "log");
    } catch (error) {
      console.error("Error fetching training results:", error);
      addLog("Error fetching training results", "error");
    }
  };

  // Cleanup interval on component unmount
  useEffect(() => {
    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [intervalId]);

  return (
    <div>
      <Button
        text="Train"
        variant="primary"
        onClick={handleTrainButton}
        disabled={loading} // Disable the button while loading
      />
      {status && <p className="text-[10px] text-sage mt-1 h-5">Status: {status}</p>}
      {results && (
          <p className="text-[10px] text-sage mt-1 h-7">
          {JSON.stringify(results, null, 2)}
      </p>
      )}
    </div>
  );
};

export default TrainButton;

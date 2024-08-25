"use client";

import React, { useState } from 'react';
import Button from '../Button'; // Adjust the import path according to your file structure
import useLogStore from "@/app/store/useLogStore";
import { InstrumentProps } from '@/app/globals';

const TrainButton: React.FC<InstrumentProps> = ({ symbol }) => {
  // State to manage the loading state of the button
  const [loading, setLoading] = useState(false);
  
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
    } catch (error) {
      console.error("Error calling /api/train:", error);
      addLog("Error calling /api/train", "error");
    } finally {
      setLoading(false); // Re-enable the button once the API call is complete
    }
  };

  return (
    <Button
      text="Train"
      variant="primary"
      onClick={handleTrainButton}
      disabled={loading} // Disable the button while loading
    />
  );
};

export default TrainButton;

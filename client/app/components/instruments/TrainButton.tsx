"use client"

import React from 'react';
import Button from '../Button'; // Adjust the import path according to your file structure
import useLogStore from "@/app/store/useLogStore";
import { InstrumentProps } from './types';

const TrainButton :React.FC<InstrumentProps> = ({ symbol }) =>{
  // Extract addLog from the useLogStore hook
  const addLog = useLogStore((state) => state.addLog);

  // Define the function to handle the train button click
  const handleTrainButton = async () => {
    addLog(`Starting training a model for ${symbol}`, "log");

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
    }
  };

  return (
    <Button
      text="Train"
      variant="primary"
      onClick={handleTrainButton} // Bind handleTrainButton to the button click
    />
  );
};

export default TrainButton;

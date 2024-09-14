"use client"

import React from 'react';
import useLogStore from "@/app/store/useLogStore";
import Button from '../Button';
import { InstrumentProps } from '@/app/globals';



const PredictButton :React.FC<InstrumentProps> = ({ symbol }) => {
  // Extract addLog from the useLogStore hook
  const addLog = useLogStore((state) => state.addLog);

  // Define the async function to handle button click
  const handlePredictButton = async () => {
    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const result = await response.json();
      addLog(`Predict API Response: ${result.message}`, "log");
    } catch (error) {
      console.error("Error calling /api/predict:", error);
      addLog("Error calling /api/predict", "error");
    }
  };

  return (
    <div>
 <Button
      text="Predict"
      variant="primary"
      onClick={handlePredictButton} // Bind handlePredictButton to the button click
    />
    </div>
   
  );
};

export default PredictButton;

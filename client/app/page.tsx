"use client";

import React, { useState } from "react";
import Button from "./components/Button";
import useLogStore from "./components/useLogStore";

interface ApiResponse {
  success: boolean;
  message: string;
  data: any;
}


const Page = () => {
  const addLog = useLogStore((state) => state.addLog);
  const [globalSymbol, setGlobalSymbol] = useState<string>("AAPL")

  const handleDownloadButton = (symbol: string) => {
    addLog("Starting download for instrument " + symbol, "log");
    const encodedSymbol = encodeURIComponent(symbol);
    const eventSource = new EventSource(`/api/download?symbol=${encodedSymbol}`);
  
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
  

  const handleTrainButton = async () => {
    try {
      const response = await fetch("/api/train", {
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
      <div style={{ display: "flex", gap: "10px" }}>
        <Button
          text="Download"
          variant="primary"
          onClick={()=>handleDownloadButton(globalSymbol)}
        />
        <Button text="Train" variant="primary" onClick={handleTrainButton} />
        <Button
          text="Predict"
          variant="primary"
          onClick={handlePredictButton}
        />
      </div>
    </div>
  );
};

export default Page;

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
  const [data, setData] = useState<ApiResponse | null>(null);
  const addLog = useLogStore((state) => state.addLog);

  const handleDownloadButton = async () => {
    addLog("downloading some data...calling /api/train", "log")
    try {
      const response = await fetch("/api/download", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const result = await response.json();
      setData(result);

      addLog(`Download API Response: ${result.message}`, "log");
    } catch (error) {
      console.error("Error calling /api/download:", error);
      addLog("Error calling /api/download", "error");
    }
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
      setData(result);

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
      setData(result);

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
          onClick={handleDownloadButton}
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

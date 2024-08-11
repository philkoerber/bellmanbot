"use client";

import React, { useState } from "react";
import Button from "./components/Button";

interface ApiResponse {
  success: boolean;
  message: string;
}

const Page = () => {
  const [data, setData] = useState<ApiResponse | null>(null);

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

      // Assuming customConsole is available globally
      if (window.customConsole) {
        window.customConsole.log(
          `Train API Response: ${result.message}`,
          "log"
        );
      }
    } catch (error) {
      console.error("Error calling /api/train:", error);
      if (window.customConsole) {
        window.customConsole.log("Error calling /api/train", "error");
      }
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

      // Assuming customConsole is available globally
      if (window.customConsole) {
        window.customConsole.log(
          `Predict API Response: ${result.message}`,
          "log"
        );
      }
    } catch (error) {
      console.error("Error calling /api/predict:", error);
      if (window.customConsole) {
        window.customConsole.log("Error calling /api/predict", "error");
      }
    }
  };

  return (
    <div>
      <div style={{ display: "flex", gap: "10px" }}>
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

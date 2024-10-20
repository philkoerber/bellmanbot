"use client";
import React, { useEffect } from "react";
import { InstrumentProps } from "@/app/globals";
import Button from "../Button";
import useDownloadStore from "@/app/store/downloadStore";
import useTrainingStore from "@/app/store/trainingStore";
import useLogStore from "@/app/store/logStore";
import TrainingBackground from "./TrainingBackground";

const Instrument: React.FC<InstrumentProps> = ({ symbol }) => {
  // STORE STUFF

  const { addLog } = useLogStore((state) => ({
    addLog: state.addLog,
  }));

  const { downloadProgress, updateDownloadProgress } = useDownloadStore(
    (state) => ({
      downloadProgress: state.downloadProgress,
      updateDownloadProgress: state.updateDownloadProgress,
    })
  );

  const { trainingProgress, updateTrainingProgress } = useTrainingStore(
    (state) => ({
      trainingProgress: state.trainingProgress,
      updateTrainingProgress: state.updateTrainingProgress,
    })
  );

  //GET THIS INSTRUMENTS SYMBOL DATA

  const getInstrumentInfo = async (symbol: string) => {
    try {
      const response = await fetch(
        `/api/instrument_info?symbol=${encodeURIComponent(symbol)}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.error || "Error in getting data for instrument"
        );
      }

      // This will log the body content directly
      const instrumentData = await response.json();
      return instrumentData;
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    const fetchInstrumentData = async () => {
      const data = await getInstrumentInfo(symbol);
      if (data) {
        // Update download progress message and status
        const dataPoints = data.data_points ?? "No data";
        updateDownloadProgress(symbol, {
          message: `Points: ${dataPoints}`,
          status: dataPoints !== "No data" ? "success" : "error",
        });

        // Extract training results if available
        const trainingResults = data.training_results || {};
        const hasTrainingResults = !!Object.keys(trainingResults).length;

        updateTrainingProgress(symbol, {
          message: hasTrainingResults
            ? `Model for ${symbol}`
            : "No model found",
          started: trainingResults.timestamp || "N/A",
          status: hasTrainingResults ? "success" : "error",
          result: {
            epoch: hasTrainingResults ? trainingResults.epoch ?? 100 : 0,
            loss: trainingResults.final_training_loss ?? "N/A",
            valLoss: trainingResults.final_validation_loss ?? "N/A",
          },
        });
      }
    };

    fetchInstrumentData();
  }, [symbol]);

  const symbolDownloadProgress = downloadProgress[symbol] || {
    message: "Loading download progress...",
    status: "",
  };

  const symbolTrainingProgress = trainingProgress[symbol] || {
    message: "Loading training process",
    status: "",
  };

  // POST METHODS

  const downloadData = async (symbol: string) => {
    addLog("Starting download of " + symbol, "log");
    try {
      const response = await fetch(`/api/download?symbol=${symbol}`, {
        method: "POST",
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Starting the download failed...");
      }
    } catch (error) {
      console.error("Error:", error);
      updateDownloadProgress(symbol, {
        message: "Starting the download failed...",
        status: "error",
      });
    }
  };

  const startTraining = async (symbol: string) => {
    addLog("Starting training of " + symbol, "log");
    try {
      const response = await fetch(`/api/train?symbol=${symbol}`, {
        method: "POST",
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Starting the training failed...");
      }
    } catch (error) {
      console.error("Error:", error);
      updateTrainingProgress(symbol, {
        message: "Starting the training failed...",
        status: "error",
      });
    }
  };

  return (
    <div className="p-2 bg-seasalt bg-opacity-70 border-pakistan border-b-2 sm:border-r-0 lg:border-r-2 gap-2 h-[200px] overflow-hidden relative">
      {/* Move TrainingBubble behind everything */}
      {symbolTrainingProgress.status === "pending" && (
        <div className="absolute w-full h-full flex justify-center items-center z-[-1]">
          <TrainingBackground />
        </div>
      )}

      <div className="flex gap-2 z-10">
        {/* DOWNLOAD */}
        <div className="basis-1/4">
          <Button
            disabled={symbolDownloadProgress.status === "pending"}
            onClick={() => downloadData(symbol)}
          >
            Download
          </Button>
          <div className="text-sm text-pakistan mt-1">
            <p>{symbolDownloadProgress.message}</p>
            <p className="text-xs font-extralight">
              {symbolDownloadProgress.status}
            </p>
          </div>
        </div>

        {/* TRAIN */}
        <div className="basis-1/2">
          <Button
            disabled={symbolTrainingProgress.status === "pending"}
            onClick={() => startTraining(symbol)}
          >
            Train
          </Button>
          <div className="z-50 text-sm text-pakistan mt-1 flex flex-col gap-1">
            <p>{symbolTrainingProgress.message}</p>
            <p className="text-xs font-extralight">
              Started: {symbolTrainingProgress.started}
            </p>
            <p className="text-xs font-extralight">
              Epoch: {symbolTrainingProgress.result?.epoch}
            </p>
            <p className="text-xs font-extralight">
              Loss: {symbolTrainingProgress.result?.loss}
            </p>
            <p className="text-xs font-extralight">
              Accuracy: {symbolTrainingProgress.result?.valLoss}
            </p>
            <p className="text-xs font-extralight">
              {symbolTrainingProgress.status}
            </p>
          </div>
        </div>

        {/* TEST AND SOME INFOS */}
        <div className="basis-1/4">
          <Button disabled={true}>Test</Button>
        </div>

        <h1 className="text-6xl text-sage select-none tracking-tighter font-extrabold absolute right-0 -bottom-2 -z-0">
          {symbol}
        </h1>
      </div>
    </div>
  );
};

export default Instrument;

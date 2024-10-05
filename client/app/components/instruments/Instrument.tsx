"use client";
import React from "react";
import { InstrumentProps } from "@/app/globals";
import Button from "../Button";
import useDownloadStore from "@/app/store/downloadStore";
import useTrainingStore from "@/app/store/trainingStore";
import useLogStore from "@/app/store/logStore";

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

  const symbolDownloadProgress = downloadProgress[symbol] || {
    message: "TODO mabe fetch metadata",
    status: "",
  };

  const symbolTrainingProgress = trainingProgress[symbol] || {
    message: "TODO mabe fetch metadata",
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
    <div className="p-1 bg-seasalt bg-opacity-70 border-sage border-2 rounded-sm gap-2 h-[200px] relative">
      <h1 className="text-5xl text-sage font-bold absolute right-1 bottom-0">
        {symbol}
      </h1>

      <div className="flex gap-2">
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
          <div className="text-sm text-pakistan mt-1">
            <p>{symbolTrainingProgress.message}</p>
            <p className="text-xs font-extralight">
              {symbolTrainingProgress.status}
            </p>
            <p className="text-xs font-extralight">
              Epoch: {symbolTrainingProgress.result?.epoch}
            </p>
            <p className="text-xs font-extralight">
              Loss: {symbolTrainingProgress.result?.loss}
            </p>
            <p className="text-xs font-extralight">
              Accuracy: {symbolTrainingProgress.result?.accuracy}
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
      </div>
    </div>
  );
};

export default Instrument;

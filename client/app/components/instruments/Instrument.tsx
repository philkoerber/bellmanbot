"use client";
import React from "react";
import { InstrumentProps } from "@/app/globals";
import Button from "../Button";
import useDownloadStore from "@/app/store/downloadStore";

const Instrument: React.FC<InstrumentProps> = ({ symbol }) => {
  const { downloadProgress, updateDownloadProgress } = useDownloadStore(
    (state) => ({
      downloadProgress: state.downloadProgress,
      updateDownloadProgress: state.updateDownloadProgress,
    })
  );

  const downloadData = async (symbol: string) => {
    try {
      const response = await fetch(`/api/download?symbol=${symbol}`, {
        method: "POST",
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Download failed");
      }
    } catch (error) {
      console.error("Error:", error);
      updateDownloadProgress(symbol, {
        message: "Download failed",
        status: "error",
      });
    }
  };

  const symbolDownloadProgress = downloadProgress[symbol] || {
    message: "TODO mabe fetch metadata",
    status: "",
  };

  return (
    <div className="p-1 bg-seasalt bg-opacity-70 border-sage border-2 rounded-sm gap-2 h-[200px] relative">
      <h1 className="text-6xl text-sage font-extralight absolute right-0 bottom-0">
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
          <Button disabled={true}>Train</Button>
        </div>

        {/* PREDICT AND SOME INFOS */}
        <div className="basis-1/4">
          <Button disabled={true}>Test</Button>
        </div>
      </div>
    </div>
  );
};

export default Instrument;

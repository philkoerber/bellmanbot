"use client";
import React from "react";
import { InstrumentProps } from "@/app/globals";
import Button from "../Button";
import useDownloadStore from "@/app/store/downloadStore";

const Instrument: React.FC<InstrumentProps> = ({ symbol }) => {
  const { progress, updateProgress } = useDownloadStore((state) => ({
    progress: state.progress,
    updateProgress: state.updateProgress,
  }));

  const downloadData = async (symbol: string) => {
    try {
      const response = await fetch(`/api/download?symbol=${symbol}`, { method: 'POST' });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Download failed');
      }
  
      const data = await response.json();
      console.log(data.message); // Log or use the message from the API response
      updateProgress(symbol, { message: 'Download started...', status: 'in-progress' });
    } catch (error) {
      console.error('Error:', error);
      updateProgress(symbol, { message: 'Download failed', status: 'error' });
    }
  };

  const symbolProgress = progress[symbol] || { message: '', status: '' };
  
  return (
    <div className="p-1 bg-seasalt bg-opacity-70 border-sage border-2 rounded-sm flex gap-2 h-[200px]">
      <div className="flex flex-col w-24 gap-2">
        <h1 className="text-xl text-pakistan font-extralight overflow-hidden whitespace-nowrap text-ellipsis">
          {symbol}
        </h1>
        <Button onClick={() => downloadData(symbol)}>Download</Button>
        <Button disabled={true}>Train</Button>
        <Button disabled={true}>Predict</Button>
        {symbolProgress.message && (
          <p className="text-sm text-pakistan">
            {symbolProgress.message} ({symbolProgress.status})
          </p>
        )}
      </div>
    </div>
  );
};

export default Instrument;

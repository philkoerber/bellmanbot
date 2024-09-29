"use client"
import React from "react";
import TrainButton from "./TrainButton";
import PredictButton from "./PredictButton";
import { InstrumentProps } from '@/app/globals';
import Button from "../Button";
import { useDownloadStore } from "@/app/store/downloadStore";

const Instrument: React.FC<InstrumentProps> = ({ symbol }) => {
  const { loading, downloadData } = useDownloadStore();

  const handleDownloadClick = () => {
    downloadData(symbol)
  };
   
  return (
    <div className="p-1 bg-seasalt bg-opacity-70 border-sage border-2 rounded-sm flex gap-2 h-[200px]">
      <div className="flex flex-col w-24 gap-2">
        <h1 className="text-xl text-pakistan font-extralight overflow-hidden whitespace-nowrap text-ellipsis">
          {symbol}
        </h1>
        <Button disabled={loading[symbol]} onClick={handleDownloadClick}>Download</Button>
        <Button disabled={true}>Train</Button>
        <Button disabled={true}>Predict</Button>
      </div>
    </div>
  );
};

export default Instrument;

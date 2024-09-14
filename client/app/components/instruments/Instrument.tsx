"use client"
import React, { useEffect, useState, useCallback } from "react";
import TrainButton from "./TrainButton";
import DownloadButton from "./DownloadButton";
import PredictButton from "./PredictButton";
import useMetadataStore from "@/app/store/useMetadataStore"; // Import the metadata store
import useLogStore from "@/app/store/useLogStore";
import { InstrumentProps, InstrumentMetadata } from '@/app/globals';
import PieChart from "./LineChart";

const Instrument: React.FC<InstrumentProps> = ({ symbol }) => {
  const addInstrument = useMetadataStore((state) => state.addInstrument);
  const addLog = useLogStore((state) => state.addLog);
  
  const [lastModified, setLastModified] = useState("Loading...");
  const [loading, setLoading] = useState(false);

  const fetchDownloadedMetadata = useCallback(async () => {
    try {
      const response = await fetch(`/api/metadata?symbol=${symbol}`);
      if (response.ok) {
        const metadata: InstrumentMetadata = await response.json();
        setLastModified(metadata.data_file?.last_modified || "No data available");
        addInstrument(symbol, metadata);
      } else {
        setLastModified("Failed to load data");
      }
    } catch (error) {
      console.error('Failed to fetch metadata:', error);
      setLastModified("Error loading data");
    }
  }, [symbol, addInstrument]);

  useEffect(() => {
    fetchDownloadedMetadata();
  }, [fetchDownloadedMetadata]);

  return (
    <div className="p-1 bg-seasalt bg-opacity-70 border-sage border-2 rounded-sm flex gap-2 h-[200px]">
      <div className="flex flex-col w-24 gap-2">
      <h1 className="text-xl text-pakistan font-extralight overflow-hidden whitespace-nowrap text-ellipsis">
  {symbol}
</h1>
        <DownloadButton
          symbol={symbol}
          lastModified={lastModified}
          setLoading={setLoading}
          loading={loading}
          fetchDownloadedMetadata={fetchDownloadedMetadata}
          addLog={addLog}
        />
        <TrainButton symbol={symbol} />
        <PredictButton symbol={symbol} />
      </div>

      <div className="h-full w-full">
        <PieChart symbol={symbol} />
      </div>
    </div>
  );
};

export default Instrument;
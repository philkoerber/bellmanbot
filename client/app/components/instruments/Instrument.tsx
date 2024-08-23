import React from "react";
import Button from "../Button";
import TrainButton from "./TrainButton";
import DownloadButton from "./DownloadButton";
import PredictButton from "./PredictButton";



interface InstrumentProps {
  symbol: string;
}

const Instrument: React.FC<InstrumentProps> = ({ symbol }) => {
  return (
    <div className="p-2 bg-seasalt bg-opacity-50 border-sage border-2 rounded-sm">
        <div className="flex flex-col w-36 gap-2">
            <h1 className="text-3xl text-pakistan font-extralight">{symbol}</h1>
            <DownloadButton symbol={symbol}/>
            <TrainButton symbol={symbol}/>
            <PredictButton symbol={symbol}/>
        </div>
        
    
      
    </div>
  );
};

export default Instrument;
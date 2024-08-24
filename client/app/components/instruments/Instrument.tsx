import React from "react";
import TrainButton from "./TrainButton";
import DownloadButton from "./DownloadButton";
import PredictButton from "./PredictButton";
import BarChart from "./BarChart";
import { useEffect } from "react";
import dummydata from "../dummydata"


interface InstrumentProps {
  symbol: string;
}

const Instrument: React.FC<InstrumentProps> = ({ symbol }) => {

  return (
    <div className="p-1 bg-seasalt bg-opacity-50 border-sage border-2 rounded-sm flex gap-2 h-[200px]">

        <div className="flex flex-col w-24 gap-2">
            <h1 className="text-xl text-pakistan font-extralight font">{symbol}</h1>
            <DownloadButton symbol={symbol}/>
            <TrainButton symbol={symbol}/>
            <PredictButton symbol={symbol}/>
        </div>

        <div className="h-full w-1/2">
          <BarChart data={[]}/>
        </div>
      
    </div>
  );
};

export default Instrument;
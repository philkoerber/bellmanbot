import React from "react";
import { forexPairs } from "./components/instruments/instruments";
import Instrument from "./components/instruments/Instrument";


const Page = () => {

  return (
    <div className="flex flex-col gap-2">
        {forexPairs.map((symbol)=>{
          return(<Instrument symbol={symbol} key={symbol}/>)
        })}
    </div>
  );
};

export default Page;

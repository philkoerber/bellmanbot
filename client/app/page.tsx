
import React, { useState, useEffect } from "react";
import { forexPairs } from "./components/instruments/instruments";
import Instrument from "./components/instruments/Instrument";

const Page = () => {

  return (
    <div className="flex flex-col gap-2">
      {forexPairs.map((symbol, index) => (
        <div
          key={symbol}
          className="opacity-0 animate-fade-in"
          style={{ animationDelay: `${index * 200}ms` }} // Sync delay with fade-in effect
        >
          <Instrument symbol={symbol} />
        </div>
      ))}
    </div>
  );
};

export default Page;
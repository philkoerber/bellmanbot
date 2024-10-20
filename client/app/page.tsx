"use client";

import React, { useEffect, useState } from "react";
import Instrument from "./components/instruments/Instrument";

const Page = () => {
  // State to hold the symbols loaded from the JSON file
  const [symbols, setSymbols] = useState([]);

  // Fetch the JSON file when the component mounts
  useEffect(() => {
    fetch("/api/instruments")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch symbols.json");
        }
        return response.json();
      })
      .then((data) => {
        setSymbols(data);
      })
      .catch((error) => {
        console.error("Error fetching the symbols:", error);
      });
  }, []);

  // Render the component with the fetched data
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2">
      {symbols.map(({ symbol }, index) => (
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

"use client"

import { create } from "zustand";
import { useEffect } from "react";

// Define the structure for metadata related to instruments
interface InstrumentMetadata {
  lastDownloadedAt: string | null;
  trainingData: TrainingData[];
}

interface TrainingData {
  timestamp: string;
  training_loss: number;
  validation_loss: number;
  accuracy: number;
  learning_rate: number;
}

// Define the structure for the store's state
interface MetadataStore {
  downloadedInstruments: { [symbol: string]: InstrumentMetadata };
  trainedInstruments: { [symbol: string]: InstrumentMetadata };
  
  // Actions to update the state
  addDownloadedInstrument: (symbol: string, metadata: InstrumentMetadata) => void;
  addTrainedInstrument: (symbol: string, metadata: InstrumentMetadata) => void;
  clearMetadata: () => void;
}

const useMetadataStore = create<MetadataStore>((set) => ({
  downloadedInstruments: {},
  trainedInstruments: {},

  // Add or update downloaded instrument metadata
  addDownloadedInstrument: (symbol, metadata) =>
    set((state) => ({
      downloadedInstruments: {
        ...state.downloadedInstruments,
        [symbol]: metadata,
      },
    })),

  // Add or update trained instrument metadata
  addTrainedInstrument: (symbol, metadata) =>
    set((state) => ({
      trainedInstruments: {
        ...state.trainedInstruments,
        [symbol]: metadata,
      },
    })),

  // Clear all metadata
  clearMetadata: () => set({ downloadedInstruments: {}, trainedInstruments: {} }),
}));

// Custom hook to initialize or fetch metadata (if necessary)
export const useInitializeMetadata = (symbol: string) => {
  const addDownloadedInstrument = useMetadataStore((state) => state.addDownloadedInstrument);
  const addTrainedInstrument = useMetadataStore((state) => state.addTrainedInstrument);

  useEffect(() => {
    // Example fetch for downloaded instrument metadata
    const fetchDownloadedMetadata = async () => {
      try {
        const response = await fetch(`/api/metadata?symbol=${symbol}`);
        if (response.ok) {
          const metadata: InstrumentMetadata = await response.json();
          addDownloadedInstrument(symbol, metadata);
        }
      } catch (error) {
        console.error('Failed to fetch metadata:', error);
      }
    };

    fetchDownloadedMetadata();

    // Example logic for fetching trained instrument metadata can be added similarly
    // const fetchTrainedMetadata = async () => { ... }

  }, [symbol, addDownloadedInstrument, addTrainedInstrument]);
};

export default useMetadataStore;
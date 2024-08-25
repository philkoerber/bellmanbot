"use client";

import { create } from "zustand";
import { InstrumentMetadata } from "../globals";

// Define the structure for the store's state
interface MetadataStore {
  instruments: { [symbol: string]: InstrumentMetadata };

  // Actions to update the state
  addInstrument: (symbol: string, metadata: InstrumentMetadata) => void;
  clearMetadata: () => void;
}

const useMetadataStore = create<MetadataStore>((set) => ({
  instruments: {},

  // Add or update instrument metadata
  addInstrument: (symbol, metadata) =>
    set((state) => ({
      instruments: {
        ...state.instruments,
        [symbol]: metadata,
      },
    })),

  // Clear all metadata
  clearMetadata: () => set({ instruments: {} }),
}));

export default useMetadataStore;

import { create } from 'zustand';
import useSocketStore from './socketStore';

interface SymbolProgress {
  message: string;
  status: string;
}

interface DownloadStore {
  progress: Record<string, SymbolProgress>;
  updateProgress: (symbol: string, data: SymbolProgress) => void;
}

const useDownloadStore = create<DownloadStore>((set) => ({
  progress: {}, // Initialize an empty object to hold progress for each symbol
  updateProgress: (symbol, data) =>
    set((state) => ({
      progress: {
        ...state.progress,
        [symbol]: data, // Dynamically update the symbol's progress
      },
    })),
}));

// Subscribe to updates from socketStore and pass to downloadStore
const socket = useSocketStore.getState().socket;
socket.on('download_progress', ({ symbol, message, status }) => {
  useDownloadStore.getState().updateProgress(symbol, { message, status });
});

export default useDownloadStore;

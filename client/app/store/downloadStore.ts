import { create } from 'zustand';
import useSocketStore from './socketStore';

interface SymbolDownloadProgress {
  message: string;
  status: string;
}

interface DownloadStore {
  downloadProgress: Record<string, SymbolDownloadProgress>;
  updateDownloadProgress: (symbol: string, data: SymbolDownloadProgress) => void;
}

const useDownloadStore = create<DownloadStore>((set) => ({
  downloadProgress: {}, // Initialize an empty object to hold progress for each symbol
  updateDownloadProgress: (symbol, data) =>
    set((state) => ({
      downloadProgress: {
        ...state.downloadProgress,
        [symbol]: data, // Dynamically update the symbol's progress
      },
    })),
}));

// Subscribe to updates from socketStore and pass to downloadStore
const socket = useSocketStore.getState().socket;
socket.on('download_progress', ({ symbol, message, status }) => {
  useDownloadStore.getState().updateDownloadProgress(symbol, { message, status });
});

export default useDownloadStore;

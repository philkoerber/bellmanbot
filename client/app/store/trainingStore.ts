import { create } from "zustand";
import useSocketStore from "./socketStore";

// Define the interface for SymbolTrainingProgress
interface SymbolTrainingProgress {
  message: string;
  started?: string; // This could represent when training started
  result?: {
    epoch: number; // The current epoch number
    loss: number; // The loss value for the current epoch
    accuracy: number; // Optional accuracy metric for the current epoch
  };
  status: "pending" | "success" | "error" | "loading";
}

// Define the interface for TrainingStore
interface TrainingStore {
  trainingProgress: Record<string, SymbolTrainingProgress>;
  updateTrainingProgress: (
    symbol: string,
    data: SymbolTrainingProgress
  ) => void;
}

// Create Zustand store for training progress
const useTrainingStore = create<TrainingStore>((set) => ({
  trainingProgress: {},
  updateTrainingProgress: (symbol, data) =>
    set((state) => ({
      trainingProgress: {
        ...state.trainingProgress,
        [symbol]: data,
      },
    })),
}));

// Subscribe to updates from socketStore and pass to TrainingStore
const socket = useSocketStore.getState().socket;
socket.on(
  "training_progress",
  ({ symbol, message, status, started, result }) => {
    // Ensure that the result includes epoch, loss, and optional accuracy
    const { epoch, loss, accuracy } = result;

    // Update the training progress in the Zustand store
    useTrainingStore.getState().updateTrainingProgress(symbol, {
      message,
      status,
      started,
      result: { epoch, loss, accuracy },
    });
  }
);

export default useTrainingStore;

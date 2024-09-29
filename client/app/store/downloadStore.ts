"use client";
import { create } from 'zustand';
import useSocketStore from './socketStore'; // Import the socketStore

interface DownloadState {
  loading: Record<string, boolean>;
  downloadData: (symbol: string) => Promise<void>;
}

export const useDownloadStore = create<DownloadState>((set) => ({
  loading: {},
  
  // Function to handle data download
  downloadData: async (symbol: string) => {
    const socket = useSocketStore.getState().socket; // Get socket from socketStore

    // Set loading state
    set((state) => ({ loading: { ...state.loading, [symbol]: true } }));

    try {
      // Trigger the download on the server
      const response = await fetch(`/api/download?symbol=${symbol}`, { method: 'POST' });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      if (data.job_id) {
        console.log(`Download started with job ID: ${data.job_id}`);

        // Listen for download status updates from the server
        socket.on('download_status', (statusData: { message: string }) => {
          console.log(`Download status: ${statusData.message}`);
        });

        // Listen for download completion
        socket.on('download_complete', (completeData: { message: string }) => {
          console.log(`Download completed: ${completeData.message}`);

          // Update loading state
          set((state) => ({
            loading: { ...state.loading, [symbol]: false },
          }));

          // Cleanup listeners when download is complete
          socket.off('download_status');
          socket.off('download_complete');
        });
      } else {
        throw new Error('No job ID received');
      }
    } catch (error: any) {
      console.error(`Error in downloading data: ${error.message}`);
    } finally {
      // Ensure loading state is set to false if there’s an error
      set((state) => ({ loading: { ...state.loading, [symbol]: false } }));
    }
  },
}));

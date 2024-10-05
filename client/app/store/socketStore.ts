import { create } from "zustand";
import { io, Socket } from "socket.io-client";
import useLogStore from "./logStore";

const addLog = useLogStore.getState().addLog; // Access the addLog function

interface SocketStore {
  socket: Socket;
  isConnected: boolean;
  connect: () => void;
}

const socket = io("http://localhost:5000", {
  transports: ["websocket"],
});

const useSocketStore = create<SocketStore>((set) => ({
  socket,
  isConnected: false,
  connect: () => {
    socket.on("connect", () => {
      set({ isConnected: true });
      addLog("Connected with SocketIO", "log"); // Log the progress
    });

    socket.on("disconnect", () => {
      set({ isConnected: false });
      addLog("Disconnected with SocketIO", "warning"); // Log the progress
    });

    // Handle 'download_progress' and log the event
    socket.on("hello_handshake", ({ message }) => {
      addLog(message, "log");
    });
  },
}));

// Call the connect method when the store is used for the first time
useSocketStore.getState().connect();

export default useSocketStore;

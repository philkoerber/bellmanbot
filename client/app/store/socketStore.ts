// stores/socketStore.ts
import { create } from 'zustand';
import { io, Socket } from 'socket.io-client';

interface SocketStore {
  socket: Socket;
  isConnected: boolean;
  connect: () => void;
  triggerTestButton: () => void; // Function to trigger the test button event
}

const socket = io('http://localhost:5000', {
  transports: ['websocket'],
});

const useSocketStore = create<SocketStore>((set) => ({
    socket,
    isConnected: false,
    connect: () => {
      socket.on('connect', () => {
        set({ isConnected: true });
        console.log('Connected to socket server');
      });
  
      socket.on('disconnect', () => {
        set({ isConnected: false });
        console.log('Disconnected from socket server');
      });
  
      // This is crucial to listen for the acknowledgment
      socket.on('test_button_response', (response) => {
        console.log('Response from server:', response);
      });
    },
    triggerTestButton: () => {
      socket.emit('test_button'); // Emit the test_button event
    },
  }));
  
  // Call the connect method when the store is used for the first time
  useSocketStore.getState().connect();
  
  export default useSocketStore;
  
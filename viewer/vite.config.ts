import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import minimist from 'minimist';

export default defineConfig(() => {
  const argv = minimist(process.argv.slice(2));

  return {
    plugins: [react()],
    base: './',
    define: {
      __SOCKET_ADDRESS__: JSON.stringify(argv.socketAddress || '127.0.0.1:8000/ws/brain-activity'),
    },
  };
});

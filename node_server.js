const express = require('express');
const http = require('http');
const path = require('path');
const { Server } = require('socket.io');
const { exec } = require('child_process');

const app = express();
const port = 3000;

// Serve the static files from the React app
app.use(express.static(path.join(__dirname, 'frontend/build')));
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: '*' } });

io.on('connection', (socket) => {
  socket.on('command', (data) => {
    console.log('received: %s', data);
    exec(`docker run --rm recovery-tool ${data}`, (err, stdout, stderr) => {
      if (err) {
        socket.emit('output', `Error: ${stderr}`);
        return;
      }
      socket.emit('output', `Output: ${stdout}`);
    });
  });
});

server.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

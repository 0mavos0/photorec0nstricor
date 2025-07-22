const express = require('express');
const path = require('path');
const { WebSocketServer } = require('ws');
const { exec } = require('child_process');

const app = express();
const port = 3000;

// Serve the static files from the React app
app.use(express.static(path.join(__dirname, 'frontend/build')));

// WebSocket server for real-time communication
const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', function connection(ws) {
  ws.on('message', function message(data) {
    console.log('received: %s', data);
    // Example: Start Docker container with received command
    exec(`docker run --rm recovery-tool ${data}`, (err, stdout, stderr) => {
      if (err) {
        ws.send(`Error: ${stderr}`);
        return;
      }
      ws.send(`Output: ${stdout}`);
    });
  });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

const express = require('express');
const path = require('path');
const { WebSocketServer } = require('ws');
const { spawn } = require('child_process');

function sanitizeArgs(data) {
  const str = data.toString().trim();
  if (!/^[a-zA-Z0-9_\-./ ]*$/.test(str)) {
    return null;
  }
  return str.length > 0 ? str.split(/\s+/) : [];
}

const app = express();
const port = 3000;

// Serve the static files from the React app
app.use(express.static(path.join(__dirname, 'frontend/build')));

// WebSocket server for real-time communication
const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', function connection(ws) {
  ws.on('message', function message(data) {
    console.log('received: %s', data);
    const args = sanitizeArgs(data);
    if (!args) {
      ws.send('Error: invalid characters in command');
      return;
    }
    const cmd = spawn('docker', ['run', '--rm', 'recovery-tool', ...args]);
    let stdout = '';
    let stderr = '';
    cmd.stdout.on('data', chunk => {
      stdout += chunk;
    });
    cmd.stderr.on('data', chunk => {
      stderr += chunk;
    });
    cmd.on('close', code => {
      if (code !== 0) {
        ws.send(`Error: ${stderr}`);
      } else {
        ws.send(`Output: ${stdout}`);
      }
    });
  });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

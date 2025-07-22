const express = require('express');
const http = require('http');
const path = require('path');
const { Server } = require('socket.io');
const { spawn } = require('child_process');

function sanitizeArgs(data) {
  const str = String(data).trim();
  if (!/^[a-zA-Z0-9_\-./ ]*$/.test(str)) {
    return null;
  }
  return str.length > 0 ? str.split(/\s+/) : [];
}

const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, 'frontend/build')));
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: '*' } });

io.on('connection', (socket) => {
  socket.on('command', (data) => {
    const args = sanitizeArgs(data);
    if (!args) {
      socket.emit('output', 'Error: invalid characters in command');
      return;
    }

    const cmd = spawn('docker', ['run', '--rm', 'recovery-tool', ...args]);
    let stdout = '';
    let stderr = '';
    cmd.stdout.on('data', (chunk) => {
      stdout += chunk;
    });
    cmd.stderr.on('data', (chunk) => {
      stderr += chunk;
    });
    cmd.on('close', (code) => {
      if (code !== 0) {
        socket.emit('output', `Error: ${stderr}`);
      } else {
        socket.emit('output', `Output: ${stdout}`);
      }
    });
  });
});

server.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});


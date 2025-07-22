const http = require('http');
const { Server } = require('socket.io');
const Client = require('socket.io-client');

describe('websocket command', () => {
  let io, clientSocket, httpServer;

  beforeAll((done) => {
    httpServer = http.createServer();
    io = new Server(httpServer);
    io.on('connection', (socket) => {
      socket.on('command', (data) => {
        socket.emit('output', `echo:${data}`);
      });
    });
    httpServer.listen(() => {
      const port = httpServer.address().port;
      clientSocket = new Client(`http://localhost:${port}`);
      clientSocket.on('connect', done);
    });
  });

  afterAll(() => {
    io.close();
    clientSocket.close();
    httpServer.close();
  });

  test('command triggers output event', (done) => {
    clientSocket.emit('command', 'test');
    clientSocket.on('output', (msg) => {
      expect(msg).toBe('echo:test');
      done();
    });
  });
});

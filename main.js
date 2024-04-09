const { app, BrowserWindow } = require('electron');
const net = require('net');
const dgram = require('dgram');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  });

  mainWindow.loadFile('index.html');

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// TCP Server
const tcpServer = net.createServer((socket) => {
  socket.on('data', (data) => {
    // Handle TCP data
  });

  socket.on('end', () => {
    // Handle TCP connection termination
  });
});

tcpServer.listen(server_port, server_address, () => {
  console.log(`TCP server running at ${server_address}:${server_port}`);
});

// UDP Server
const udpServer = dgram.createSocket('udp4');

udpServer.on('error', (err) => {
  console.log(`UDP server error:\n${err.stack}`);
  udpServer.close();
});

udpServer.on('message', (msg, rinfo) => {
  // Handle UDP messages
});

udpServer.on('listening', () => {
  const address = udpServer.address();
  console.log(`UDP server running at ${address.address}:${address.port}`);
});

udpServer.bind(server_port, server_address);

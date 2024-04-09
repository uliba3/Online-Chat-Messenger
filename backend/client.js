const {tcpClient, enterRoom} = require('../tcpClient');
const {udpClient, sendMessage} = require('../udpClient');
const {tcpServerPort, address} = require('../config');

tcpClient.connect(tcpServerPort, address, () => {
    console.log('Connected to TCP server');
    enterRoom('room1', 'user1');
});

tcpClient.on('data', (data) => {
    console.log('Received data from server:', data.toString());
    if (data.toString().trim() === 'success!!') {
        sendMessage('room1 user1 Entered The room!');
    }
});
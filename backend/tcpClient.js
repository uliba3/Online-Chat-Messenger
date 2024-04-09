const net = require('net');
const { tcpServerPort, address } = require('../config.js');

const client = new net.Socket();

function enterRoom(roomName, userName) {
    client.write(`${roomName} ${userName}`);
    console.log(`Entered room ${roomName} as ${userName}`);
}


client.on('close', () => {
    console.log('Connection closed');
});

module.exports = {
    enterRoom: enterRoom,
    tcpClient: client // corrected export syntax
};
const dgram = require('dgram');

// Create a UDP socket
const client = dgram.createSocket('udp4');

const { address, udpServerPort } = require('../config.js');

function sendMessage(message) {
    client.send(message, udpServerPort, address, (error) => {
        if (error) {
            console.error('Error sending message:', error);
            client.close();
        } else {
            console.log('Message sent to server:', message);
        }
    });
}

// Handle incoming messages from the server
client.on('message', (msg, rinfo) => {
    console.log('Received message from server:', msg.toString());
});

// Handle errors
client.on('error', (error) => {
    console.error('UDP client error:', error);
    client.close();
});

// Close the socket when done
client.on('close', () => {
    console.log('UDP client socket closed');
});

module.exports = {
    sendMessage: sendMessage,
    udpClient: client
};
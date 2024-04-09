const dgram = require('dgram');
const { updateData, readData } = require('./dataUpdater.js');
const { udpServerPort, address } = require('./config.js');

// Create a UDP server
const server = dgram.createSocket('udp4');

server.bind(udpServerPort, address);

// Handle incoming messages
server.on('message', (data, rinfo) => {
    console.log(`Received message: ${data} from ${rinfo.address}:${rinfo.port}`);
    data = data.toString().trim().split(' ');
    chatRoom = readData();
    const roomName = data[0];
    const userName = data[1];
    const newMessage = data.slice(2).join(' '); // Fix: Use slice method to extract elements from index 2 to the end and join them with a space
    rinfo = { "address": rinfo.address, "port": rinfo.port };

    message = {
        "name": userName,
        "message": newMessage
    };

    if(!chatRoom[roomName]) {
        console.log('Room does not exist');
    }else if(!chatRoom[roomName]["members"][userName]) {
        console.log('User does not exist');
    }else{
        chatRoom[roomName]["members"][userName] = rinfo;
        chatRoom[roomName]["messages"].push(message);
    }
    updateData(JSON.stringify(chatRoom));
    for (const member in chatRoom[roomName]["members"]) {
        if (chatRoom[roomName]["members"].hasOwnProperty(member)) {
            const memberInfo = chatRoom[roomName]["members"][member];
            server.send(data, memberInfo.port, memberInfo.address, (error) => {
                if (error) {
                    console.error('Error sending message:', error);
                    server.close();
                } else {
                    console.log('Message sent to client:', data.toString());
                }
            });
        }
    }
    server.send(data, rinfo.port, rinfo.address, (error) => {
        if (error) {
            console.error('Error sending message:', error);
            server.close();
        } else {
            console.log('Message sent to client:', data.toString());
        }
    });
});

// Handle server listening event
server.on('listening', () => {
    console.log(`UDP server listening on ${address}:${udpServerPort}`);
});

exports.udpServer = server;
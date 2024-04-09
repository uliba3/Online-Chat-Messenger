const net = require('net');
const { updateData, readData } = require('./dataUpdater.js');
const { tcpServerPort } = require('./config.js');

const server = net.createServer();

server.on('connection', (socket) => {
    socket.write('Welcome to the chat server!\n');

    socket.on('data', (data) => {
        console.log('Received data:', data.toString());
        data = data.toString().trim().split(' ');
        if (data.length !== 2) {
            socket.write('Invalid data format. Please provide room name and username separated by space.\n');
            return;
        }
        chatRoom = readData();
        const [roomName, userName] = data;
        console.log('Room name:', roomName);
        console.log('User name:', userName);

        // Ensure roomName and userName are non-empty
        if (!roomName || !userName) {
            socket.write('Room name and username cannot be empty.\n');
            return;
        }

        if (!chatRoom[roomName]) {
            chatRoom[roomName] = {
                "members": {
                    userName: {
                        "address": socket.remoteAddress,
                        "port": socket.remotePort
                    }
                },
                "messages": []
            };
        }else{
            chatRoom[roomName].members[userName] = {
                "address": socket.remoteAddress,
                "port": socket.remotePort
            };
        }
        updateData(JSON.stringify(chatRoom));
        socket.write('success!!');
    });

    socket.on('end', () => {
        // Remove the client from all rooms
        for (const roomName in chatRoom) {
            if (chatRoom.hasOwnProperty(roomName)) {
                delete chatRoom[roomName].members[userName];
            }
        }
        updateData(JSON.stringify(chatRoom));
    });

    socket.on('error', (err) => {
        console.error('Socket error:', err);
    });
});

server.listen(tcpServerPort, () => {
    console.log(`TCP server is listening on port ${tcpServerPort}`);
});

exports.tcpServer = server;
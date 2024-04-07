import socket
import server_config
import threading
import time
import secrets
import string

chatRooms = {
    'room1': {
        'host': None,
        'members': {}
    }
}

def generate_token(max_bytes=255):
    max_chars = max_bytes // 4  # Since each ASCII character is 1 byte, and UTF-8 uses at most 4 bytes per character
    characters = string.ascii_letters + string.digits
    length = min(max_chars, 16)  # Minimum length of 16 characters
    return ''.join(secrets.choice(characters) for _ in range(length))

def create_response(code, token):
    return code.to_bytes(1, "big") + token.encode('utf-8')

def handle_room():
    while True:
        print("waiting for connection")
        connection, client_address = room_sock.accept()
        if connection:
            header = connection.recv(32)
            if not header:
                print("Client disconnected or empty header received")
                break

            print('Received header: {}'.format(header))
            roomName_len = int.from_bytes(header[:1], "big")
            operation = int.from_bytes(header[1:2], "big")
            state = int.from_bytes(header[2:3], "big")
            operationPayload_len = int.from_bytes(header[3:], "big")

            body = connection.recv(roomName_len + operationPayload_len)
            roomName = body[:roomName_len].decode('utf-8')
            operationPayload = body[roomName_len:].decode('utf-8')
            print('Received roomName: {}, operation: {}, state: {}, operationPayload: {}'.format(roomName, operation, state, operationPayload))

            token = generate_token()
            print('Generated token: {}'.format(token))
            if operation == 1:
                print('operation is 1')
                if roomName in chatRooms:
                    if chatRooms[roomName]['host'] is None:
                        chatRooms[roomName]['host'] = {token: client_address}
                        print('{} became the host in room {}'.format(operationPayload, roomName))
                        state = 1
                    else:
                        state = 0
                        print('Room {} already exists'.format(roomName))
                else:
                    chatRooms[roomName] = {'host': {token: client_address}, 'members': {}}
                    state = 1
                    print('Host {} created room {}'.format(operationPayload, roomName))
            elif operation == 2:
                print('operation is 2')
                if roomName in chatRooms:
                    state = 1
                    chatRooms[roomName]['members'][token] = client_address
                    print('{} joined room {}'.format(operationPayload, roomName))
                else:
                    state = 0
                    print('Room {} does not exist'.format(roomName))
            response = create_response(state, token)
            connection.send(response)
            print('chatRooms: {}'.format(chatRooms))

def handle_chat():
    while True:
        try:
            data, address = chat_sock.recvfrom(4096)
            print('Received data from {}: {}'.format(address, data))
            roomName_len = int.from_bytes(data[:1], "big")
            token_len = int.from_bytes(data[1:2], "big")
            roomName = data[2:2+roomName_len].decode('utf-8')
            token = data[2+roomName_len:2+roomName_len+token_len].decode('utf-8')
            message = data[2+roomName_len+token_len:].decode('utf-8')
            print('Received roomName: {}, token: {}, message: {}'.format(roomName, token, message))
            if roomName in chatRooms:
                for memberToken in chatRooms[roomName]['members']:
                    if memberToken == token:
                        chatRooms[roomName]['members'][memberToken] = address
                    chat_sock.sendto(message.encode('utf-8'), chatRooms[roomName]['members'][memberToken])
                    print('Sent message to member {} address {}'.format(memberToken, address))
                for hostToken in chatRooms[roomName]['host']:
                    if hostToken == token:
                        chatRooms[roomName]['host'][hostToken] = address
                    chat_sock.sendto(message.encode('utf-8'), chatRooms[roomName]['host'][hostToken])
                    print('Sent message to host {} address {}'.format(hostToken, address))
            else:
                print('Room {} does not exist'.format(roomName))
        except Exception as e:
            print('Error(handle-chat): ' + str(e))

#start room server
room_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = server_config.SERVER_ADDRESS
server_port = server_config.TCP_PORT_NUMBER
room_sock.bind((server_address, server_port))
room_sock.listen(5)  # Number of connections to queue up before refusing new connections
print('Room server started on {}:{}'.format(server_address, server_port))

#start chat server
chat_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = server_config.SERVER_ADDRESS
server_port = server_config.UDP_PORT_NUMBER
chat_sock.bind((server_address, server_port))
print('Chat server started on {}:{}'.format(server_address, server_port))
        

# Create a new thread for each connection
tcp_thread = threading.Thread(target=handle_room)
udp_thread = threading.Thread(target=handle_chat)
tcp_thread.start()
udp_thread.start()

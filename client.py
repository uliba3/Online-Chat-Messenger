import socket
import threading
import server_config

SERVER_ADDRESS = server_config.SERVER_ADDRESS
TCP_PORT_NUMBER = server_config.TCP_PORT_NUMBER
UDP_PORT_NUMBER = server_config.UDP_PORT_NUMBER

def create_header_room(roomName_bytes, operation, state, operationPayload_bytes):
    return len(roomName_bytes).to_bytes(1, "big") + operation.to_bytes(1, "big") + state.to_bytes(1, "big") + len(operationPayload_bytes).to_bytes(29, "big")

def create_body_room(roomName_bytes, operationPayload_bytes):
    return roomName_bytes + operationPayload_bytes

def create_header_message(roomName_bytes, token):
    return len(roomName_bytes).to_bytes(1, "big") + len(token).to_bytes(1, "big")

def create_body_message(roomName_bytes, token, message_bytes):
    return roomName_bytes + token.encode('utf-8') + message_bytes

def join_room():
    global token
    global roomName
    global state
    while True:
        if token == 0:
            tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_sock.connect((SERVER_ADDRESS, TCP_PORT_NUMBER))
            roomName = input('Type in room name: ')
            roomName_bytes = roomName.encode('utf-8')
            operation = int(input('Do you want to be a host? 1. yes, 2. no: '))
            operationPayload = input('Type in your username: ')
            operationPayload_bytes = operationPayload.encode('utf-8')

            header = create_header_room(roomName_bytes, operation, state, operationPayload_bytes)
            body = create_body_room(roomName_bytes, operationPayload_bytes)
            tcp_sock.send(header + body)
            print('Sent join room request')
            response = tcp_sock.recv(256)
            state = int.from_bytes(response[:1], "big")
            token = response[1:].decode('utf-8')
            if state == 0:
                token = 0
                print('You are not in the room')
                tcp_sock.close()
            elif state == 1:
                message_bytes = "newbie in the room".encode('utf-8')
                header = create_header_message(roomName_bytes, token)
                body = create_body_message(roomName_bytes, token, message_bytes)
                udp_sock.sendto(header + body, (SERVER_ADDRESS, UDP_PORT_NUMBER))

def send_message():
    global token
    while True:
        if token != 0:
            message = input('Type in message: ')
            message_bytes = message.encode('utf-8')
            roomName_bytes = roomName.encode('utf-8')
            header = create_header_message(roomName_bytes, token)
            body = create_body_message(roomName_bytes, token, message_bytes)
            udp_sock.sendto(header + body, (SERVER_ADDRESS, UDP_PORT_NUMBER))

def receive_message():
    global token
    while True:
        if token != 0:
            print('Waiting for message...')
            message, _ = udp_sock.recvfrom(4094)
            print('Received: {}'.format(message.decode('utf-8')))

if __name__ == "__main__":
    state = 0
    token = 0
    roomName = None

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    join_thread = threading.Thread(target=join_room)
    send_thread = threading.Thread(target=send_message)
    receive_thread = threading.Thread(target=receive_message)

    join_thread.start()
    send_thread.start()
    receive_thread.start()

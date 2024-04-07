import socket
import sys
import threading
import server_config

def receive_messages(sock):
    while True:
        packet, addr = sock.recvfrom(4096)  # Receive data from the server
        print(packet.decode('utf-8'))  # Print the received message
        usernamelen = int.from_bytes(packet[:1], "big")
        username = packet[1:usernamelen+1].decode('utf-8')
        message = packet[usernamelen+1:].decode('utf-8')
        print('{}: {}'.format(username, message))

def protocol_header(usernamelen):
    return usernamelen.to_bytes(1, "big")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = server_config.SERVER_ADDRESS
server_port = server_config.PORT_NUMBER

print('connecting to {}:{}'.format(server_address, server_port))

try:
    # Start a new thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    receive_thread.daemon = True
    receive_thread.start()

    # Since UDP is connectionless, we don't need to connect.
    # We just send packets to the server's address and port.
    username = input('Type in your username: ')
    username_bytes = username.encode('utf-8')
    
    while True:
        message = input('Type in the message: ')
        message_bytes = message.encode('utf-8')
        
        header = protocol_header(len(username_bytes))
        packet = len(username_bytes).to_bytes(1, "big") + username_bytes + message_bytes
        sock.sendto(packet, (server_address, server_port))

finally:
    print('closing socket')
    sock.close()

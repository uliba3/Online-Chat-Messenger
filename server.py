import socket
import server_config
import threading
import time

# Dictionary to store connected clients and their last message times
connected_clients = {}

def broadcast_message(packet, sender_address):
    for address in connected_clients.keys():
        if address != sender_address:
            sock.sendto(packet, address)

def handle_client_message(packet, address):
    usernamelen = int.from_bytes(packet[:1], "big")
    username = packet[1:usernamelen+1].decode('utf-8')
    message = packet[usernamelen+1:].decode('utf-8')
    print('Received message from {}: {}'.format(username, message))
    broadcast_message(packet, address)
    connected_clients[address] = time.time()

def cleanup_clients():
    while True:
        current_time = time.time()
        for address, last_message_time in list(connected_clients.items()):
            if current_time - last_message_time > server_config.CLIENT_TIMEOUT:
                print('Client {} timed out and removed'.format(address))
                del connected_clients[address]
        time.sleep(server_config.CLEANUP_INTERVAL)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = server_config.SERVER_ADDRESS
server_port = server_config.PORT_NUMBER
sock.bind((server_address, server_port))
print('Server started on {}:{}'.format(server_address, server_port))

# Start a thread to clean up inactive clients
cleanup_thread = threading.Thread(target=cleanup_clients)
cleanup_thread.daemon = True
cleanup_thread.start()

while True:
    packet, address = sock.recvfrom(4096)
    handle_client_message(packet, address)

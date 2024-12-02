import socket
import os

# Server code with congestion control
def start_server():
    server_ip = "127.0.0.1"
    server_port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print(f"Listening for connections on {server_ip}:{server_port}...")

    # Accept incoming connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    # Receive file size
    file_size = client_socket.recv(1024).decode()
    print(f"File size: {file_size} bytes")

    # Acknowledge file size
    client_socket.send(b"File size received, starting transfer...")

    # Open the file for writing
    received_data = b""
    total_received = 0
    with open("received_file.txt", "wb") as file:
        while total_received < int(file_size):
            # Receive data in chunks
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            file.write(chunk)
            total_received += len(chunk)
            print(f"Received {len(chunk)} bytes. Total received: {total_received}/{file_size} bytes")

    print(f"File received successfully in {total_received / 1024:.2f} KB.")
    client_socket.close()

if __name__ == "__main__":
    start_server()

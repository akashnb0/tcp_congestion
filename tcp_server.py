import socket
import os

# Set server details
host = '127.0.0.1'
port = 5000
buffer_size = 1024  # Size of each packet

def start_server():
    # Create socket object
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    print(f"Listening for connections on {host}:{port}...")

    # Accept incoming connection from the client
    client_socket, client_address = s.accept()
    print(f"Connection from {client_address} established.")

    # Receive the file details
    file_info = client_socket.recv(buffer_size).decode()
    file_name, file_size = file_info.split('|')
    file_size = int(file_size)

    # Open file to write the received data
    with open(f"received_{file_name}", "wb") as file:
        print(f"Receiving file: {file_name} ({file_size} bytes)")
        
        received_data = b""
        chunks_received = set()  # To track received chunks
        chunk_size = 1024
        total_chunks = file_size // chunk_size + (1 if file_size % chunk_size else 0)

        # Receive data chunks
        while len(received_data) < file_size:
            data = client_socket.recv(buffer_size)
            if data:
                chunk_number = len(received_data) // chunk_size  # Calculate chunk number
                if chunk_number not in chunks_received:
                    file.write(data)
                    received_data += data
                    chunks_received.add(chunk_number)
                    print(f"Received chunk {chunk_number + 1}/{total_chunks}")
                else:
                    print(f"Duplicate chunk {chunk_number + 1} received. Skipping...")
            else:
                break

        print("File received successfully.")
        client_socket.close()

if __name__ == "__main__":
    start_server()

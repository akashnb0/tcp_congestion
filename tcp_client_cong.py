import socket
import os
import random
import time

# Client code with congestion control
def start_client():
    server_ip = "127.0.0.1"
    server_port = 5000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    file_name = "sample_file.txt"
    
    # Get the file size
    file_size = os.path.getsize(file_name)
    
    # Send the file size first
    client_socket.send(str(file_size).encode())

    # Wait for server confirmation that it has received the file size
    ack = client_socket.recv(1024)
    print(ack.decode())  # Print the server acknowledgment

    # Implementing slow start (exponential increase in window size)
    cwnd = 1  # Initial congestion window size (1 chunk)
    max_cwnd = 16  # Maximum window size (limit to 16 chunks)
    chunk_size = 1024  # 1 KB chunk size
    total_sent = 0

    # Send the file data in chunks
    with open(file_name, "rb") as file:
        while total_sent < file_size:
            # Send up to the current congestion window size
            for _ in range(cwnd):
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                # Simulate packet loss (10% chance of packet loss)
                if random.random() < 0.1:  # 10% packet loss
                    print("Packet lost. Skipping this chunk.")
                    continue

                # Send the chunk
                client_socket.send(chunk)
                total_sent += len(chunk)
                print(f"Sent {len(chunk)} bytes. Total sent: {total_sent}/{file_size} bytes")

            # Wait for acknowledgment from the server before increasing window size
            ack = client_socket.recv(1024).decode()

            # Exponentially increase the window size if not reached max
            if cwnd < max_cwnd:
                cwnd *= 2
            print(f"Congestion window: {cwnd} chunks")

            time.sleep(0.1)  # Simulate a small delay

    print(f"File {file_name} sent successfully.")
    client_socket.close()

if __name__ == "__main__":
    start_client()

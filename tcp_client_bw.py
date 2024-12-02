import socket
import os
import random
import time


def start_client():
    server_ip = "127.0.0.1"
    server_port = 5000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    file_name = "sample_file.txt"
    
    file_size = os.path.getsize(file_name)
    
    client_socket.send(str(file_size).encode())

    ack = client_socket.recv(1024)
    print(ack.decode())  # Server ACK

    # SLOW START
    cwnd = 1  # Initial congestion window size (1 chunk)
    max_cwnd = 16  # Maximum window size (limit to 16 chunks)
    chunk_size = 1024  # 1 KB chunk size
    total_sent = 0

    bandwidth_levels = [0.1, 0.3, 0.5, 0.7, 1.0]  # Bandwidth levels (simulated)
    current_bandwidth = random.choice(bandwidth_levels)  # Choose an initial bandwidth level

    with open(file_name, "rb") as file:
        while total_sent < file_size:
            
            for _ in range(cwnd):
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                if random.random() < 0.1:  # 10% packet loss
                    print("Packet lost. Skipping this chunk.")
                    continue


                client_socket.send(chunk)
                total_sent += len(chunk)
                print(f"Sent {len(chunk)} bytes. Total sent: {total_sent}/{file_size} bytes")

            ack = client_socket.recv(1024).decode()


            if cwnd < max_cwnd:
                cwnd *= 2
            print(f"Congestion window: {cwnd} chunks")


            current_bandwidth = random.choice(bandwidth_levels)
            delay = 1 / current_bandwidth  # Simulate bandwidth effect: lower delay = higher bandwidth
            print(f"Simulated bandwidth: {current_bandwidth} (Delay: {delay}s)")

            time.sleep(delay)

    print(f"File {file_name} sent successfully.")
    client_socket.close()

if __name__ == "__main__":
    start_client()

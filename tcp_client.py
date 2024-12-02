import socket
import os
from tqdm import tqdm
import time
import random  # For simulating packet loss

# Set server details
host = '127.0.0.1'
port = 5000
file_name = 'sample_file.txt'
packet_loss_probability = 0.5  # 50% chance to drop a packet (increased for testing)

def simulate_packet_loss():
    """Simulate packet loss with a given probability."""
    return random.random() < packet_loss_probability

def simulate_congestion_control(chunk_size):
    """Simulate congestion control by introducing a delay after each chunk."""
    time.sleep(0.1)  # Artificial delay after each chunk

def start_client():
    # Create the socket object
    s = socket.socket()
    print(f"Connecting to {host}:{port}")
    s.connect((host, port))

    # Get the file size
    file_size = os.path.getsize(file_name)
    print(f"File size: {file_size} bytes")

    # Send file details
    s.send(f"{file_name}|{file_size}".encode())

    # Open the file to read
    with open(file_name, "rb") as file:
        # Initialize progress bar
        progress = tqdm(range(file_size), f"Sending {file_name}", unit="B", unit_scale=True)

        # Send data in chunks
        chunk_size = 1024  # Starting chunk size (1KB)
        chunk_number = 0  # To track which chunk is being sent
        while True:
            # Read a chunk of data
            data = file.read(chunk_size)
            if not data:
                break  # End of file

            # Simulate packet loss
            if simulate_packet_loss():
                print(f"Packet {chunk_number} lost. Skipping this chunk.")  # Print which packet is lost
                chunk_number += 1
                continue  # Drop this chunk (simulate packet loss)

            # Send the chunk of data
            s.send(data)

            # Update progress bar
            progress.update(len(data))

            # Simulate congestion control (delay after each chunk)
            simulate_congestion_control(chunk_size)

            # Dynamically adjust the chunk size (simple control logic)
            if chunk_size < 8192:  # Max chunk size
                chunk_size += 1024  # Gradually increase chunk size

            # Increment the chunk number
            chunk_number += 1

    print("File sent successfully.")
    s.close()

if __name__ == "__main__":
    start_client()

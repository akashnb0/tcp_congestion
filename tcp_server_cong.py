import socket
import time

def start_server():
    server_ip = "127.0.0.1"
    server_port = 5000

    # Create the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow address reuse to avoid 'Address already in use' error
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the address and port
    try:
        server_socket.bind((server_ip, server_port))
    except OSError as e:
        print(f"Error binding socket: {e}")
        server_socket.close()
        return

    server_socket.listen(1)
    print(f"Listening for connections on {server_ip}:{server_port}...")

    # Accept incoming connection
    conn, addr = server_socket.accept()
    print(f"Connection from {addr} established.")

    # Receive file size first
    file_size = conn.recv(1024).decode()  # Receive file size as string
    try:
        file_size = int(file_size)  # Convert to integer
    except ValueError:
        print("Error: Invalid file size received.")
        conn.close()
        return

    # Acknowledge the file size received
    conn.send("File size received, starting transfer...".encode())
    print(f"Receiving file of size {file_size} bytes...")

    # Receive the file data in chunks
    with open("received_file.txt", "wb") as file:
        total_received = 0
        while total_received < file_size:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)
            total_received += len(data)
            print(f"Received {total_received} bytes...")

            # Send acknowledgment after each chunk is received
            conn.send(f"Received {len(data)} bytes".encode())

    print("File received successfully.")
    conn.close()

    # Close the server socket after finishing
    server_socket.close()

if __name__ == "__main__":
    start_server()

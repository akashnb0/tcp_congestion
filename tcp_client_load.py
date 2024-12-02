import socket
import time

def start_client():
    server_ip = '127.0.0.1'
    server_port = 5000  # Load balancer's port
    
    # Create a socket for client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    # Send a request to the load balancer
    request = "Hello, I'm Akash"
    print(f"Sending request: {request}")
    client_socket.send(request.encode())

    # Receive the response from the load balancer (which will forward it from backend)
    response = client_socket.recv(1024).decode()
    print(f"Received response: {response}")

    # Close the client connection
    client_socket.close()

if __name__ == '__main__':
    start_client()

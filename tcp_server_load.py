import socket
import threading
import time
import random

# Simulated backend server function
def backend_server(server_id, port):
    backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend_socket.bind(('127.0.0.1', port))
    backend_socket.listen(1)
    print(f"Backend server {server_id} listening on port {port}...")

    while True:
        client_socket, client_address = backend_socket.accept()
        print(f"Backend server {server_id} connected to {client_address}")
        data = client_socket.recv(1024).decode()
        
        # Simulate processing time and return a response
        time.sleep(random.uniform(0.5, 1.5))  # Simulating processing delay
        response = f"Server {server_id} processed: {data}"
        
        client_socket.send(response.encode())
        client_socket.close()

# Load balancer to distribute requests among backend servers
def load_balancer():
    backend_ports = [6001, 6002, 6003]  # Three backend servers
    backend_index = 0

    load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer_socket.bind(('127.0.0.1', 5000))
    load_balancer_socket.listen(5)
    print("Load balancer listening on 127.0.0.1:5000...")

    while True:
        client_socket, client_address = load_balancer_socket.accept()
        print(f"Load balancer received connection from {client_address}")

        # Forward the client's request to a backend server (round-robin)
        backend_port = backend_ports[backend_index]
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect(('127.0.0.1', backend_port))
        
        data = client_socket.recv(1024).decode()
        backend_socket.send(data.encode())

        # Receive response from backend and send it back to the client
        response = backend_socket.recv(1024).decode()
        client_socket.send(response.encode())

        backend_socket.close()
        client_socket.close()

        # Round-robin logic to choose next backend server
        backend_index = (backend_index + 1) % len(backend_ports)

# Main function to start backend servers and load balancer
def start():
    # Start backend servers in separate threads
    backend_server_threads = []
    for i in range(1, 4):
        port = 6000 + i
        thread = threading.Thread(target=backend_server, args=(i, port))
        thread.daemon = True
        thread.start()
        backend_server_threads.append(thread)

    # Start the load balancer
    load_balancer_thread = threading.Thread(target=load_balancer)
    load_balancer_thread.daemon = True
    load_balancer_thread.start()

    # Keep the program running
    while True:
        time.sleep(1)

if __name__ == '__main__':
    start()

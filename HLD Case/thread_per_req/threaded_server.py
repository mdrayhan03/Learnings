import socket
import threading
import time
import os

HOST = "127.0.0.1"
PORT = 8080
SIMULATED_DB_LAG = 2.0  # Seconds the thread will block waiting for "I/O"

def handle_client(client_socket: socket.socket, client_address: tuple, request_id: int):
    """Worker function executed inside a dedicated OS thread context."""
    thread_name = threading.current_thread().name
    print(f"[THREAD OPEN] {thread_name} handling request #{request_id} from {client_address}")
    
    try:
        # Read the incoming HTTP request payload raw bytes
        raw_request = client_socket.recv(1024).decode('utf-8')
        
        # --- SIMULATED BLOCKING I/O BOUNDARY ---
        # The thread drops into an idle, blocked state. It cannot process anything else.
        time.sleep(SIMULATED_DB_LAG)
        # ----------------------------------------
        
        # Prepare a standard HTTP text response payload
        response_body = f"Hello from Thread-per-Request Server!\nProcessed by: {thread_name}\nRequest ID: {request_id}"
        http_response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{response_body}"
        )
        
        # Send data back over the socket wire
        client_socket.sendall(http_response.encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Exception on request #{request_id}: {e}")
    finally:
        # Securely close the connection channel and exit the thread loop
        client_socket.close()
        print(f"[THREAD CLOSE] {thread_name} finished request #{request_id}. Active System Threads: {threading.active_count() - 1}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow instant socket address reuse on restart to avoid bind crashes
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(128)
    
    print(f"[*] Thread-per-Request Engine running on http://{HOST}:{PORT}")
    print(f"[*] Main Server Process PID: {os.getpid()}")
    
    request_counter = 0
    try:
        while True:
            # Main event loop blocks waiting for a new client TCP connection handshake
            client_sock, client_addr = server_socket.accept()
            request_counter += 1
            
            # SPAWN A NEW OPERATING SYSTEM THREAD FOR THE NEW CLIENT
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_sock, client_addr, request_counter),
                name=f"WorkerThread-{request_counter}"
            )
            # Start the thread execution context
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\nShutting down multi-threaded socket server engine...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
import socket

def start_server():
    # 1. Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 2. Bind the socket to a port and listen
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(1)
    print("Server is listening on http://127.0.0.1:8080 ...")

    while True:
        # 3. Wait for a client connection (Request-Response cycle begins)
        client_connection, client_address = server_socket.accept()
        
        # 4. Read the raw text request from the client
        request_data = client_connection.recv(1024).decode('utf-8')
        print("\n--- RECEIVED RAW REQUEST ---")
        print(request_data)
        print("--- END ---")
        
        # 5. Parse the request path (Basic string manipulation)
        lines = request_data.split("\r\n")
        if len(lines) > 0 and lines[0] != "":
            request_line = lines[0]
            method, path, http_version = request_line.split(" ")
            
            # 6. Basic Routing Logic
            if path == "/":
                response_body = "<h1>Welcome to the Home Page!</h1>"
                status = "200 OK"
            elif path == "/status":
                response_body = "<h1>Server status: Operational</h1>"
                status = "200 OK"
            else:
                response_body = "<h1>404 Not Found</h1>"
                status = "404 NOT FOUND"
        else:
            response_body = "<h1>Bad Request</h1>"
            status = "400 BAD REQUEST"

        # 7. Construct the raw HTTP response
        response = f"HTTP/1.1 {status}\r\n"
        response += "Content-Type: text/html\r\n"
        response += f"Content-Length: {len(response_body)}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"  # Crucial blank line separating headers from body
        response += response_body

        # 8. Send response back to client and close connection
        client_connection.sendall(response.encode('utf-8'))
        client_connection.close()

if __name__ == "__main__":
    start_server()
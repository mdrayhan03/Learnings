import asyncio
import os
import threading
import time

HOST = "127.0.0.1"
PORT = 8081
SIMULATED_DB_LAG = 2.0  # Seconds the loop will yield during "I/O"

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, request_id: int):
    """Asynchronous worker task running cooperatively on the single main thread."""
    current_thread = threading.current_thread().name
    print(f"[TASK OPEN] Processing request #{request_id} on thread: '{current_thread}'")
    
    try:
        # Read incoming raw request header bytes asynchronously
        raw_data = await reader.read(1024)
        
        # --- SIMULATED NON-BLOCKING I/O BOUNDARY ---
        # 'await' relinquishes control back to the event loop instantly.
        # The single main thread leaves this task and accepts other users.
        await asyncio.sleep(SIMULATED_DB_LAG)
        # --------------------------------------------
        
        # Build the standard text response block
        response_body = f"Hello from the Async Event Loop Server!\nProcessed on Thread: {current_thread}\nRequest ID: {request_id}"
        http_response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{response_body}"
        )
        
        # Write response data back out to the client socket channel
        writer.write(http_response.encode('utf-8'))
        await writer.drain()
    except Exception as e:
        print(f"[ERROR] Exception on request #{request_id}: {e}")
    finally:
        # Gracefully drop the socket connection channel
        writer.close()
        await writer.wait_closed()
        print(f"[TASK CLOSE] Finished request #{request_id}. Active OS Threads: {threading.active_count()}")

async def start_server():
    # Bind the asynchronous stream listener to the local port
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, next(request_counter)), 
        HOST, 
        PORT
    )
    
    print(f"[*] Async Event Loop Engine running on http://{HOST}:{PORT}")
    print(f"[*] Main Server Process PID: {os.getpid()}")
    print(f"[*] Initial Active OS Threads: {threading.active_count()}")
    
    async with server:
        await server.serve_forever()

def request_id_generator():
    """Simple counter generator for tracing request lineages."""
    n = 1
    while True:
        yield n
        n += 1

if __name__ == "__main__":
    request_counter = request_id_generator()
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\nShutting down async event loop engine...")
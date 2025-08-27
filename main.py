import socket  # noqa: F401
import threading
import os
import sys
def handle_client(client_socket):
     success_response = 'HTTP/1.1 200 OK\r\n\r\n'
     notfound_response = 'HTTP/1.1 404 Not Found\r\n\r\n'
     try:
          data = client_socket.recv(1024)
          data_header = data.decode().split(" ")
          if len(data_header) > 1:
               path = data_header[1]
          else:
               path = ''
          if path == '/':
               client_socket.send(success_response.encode())
          elif path == "/user-agent":
               lines = data.decode().split("\r\n")
               for line in lines:
                    if line.startswith("User-Agent"):
                         content_body =  line.split(":")[1].strip()
               response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    f"Content-Length: {len(content_body)}\r\n"
                    "\r\n"
                    f"{content_body}"
               )
               client_socket.sendall(response.encode())
          elif path.startswith('/files/'):
               filename = path.split("/")[2]
               if len(sys.argv) > 1:
                    directory = sys.argv[2]
               filepath = f"{directory}{filename}"
               print(filepath)
               if os.path.exists(filepath):
                    size = os.path.getsize(filepath)
                    with open(filepath, "r") as f:
                         contents = f.read()
                    response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {size}\r\n"
                    "\r\n"
                    f"{contents}"
                    )
               else:
                    response = (
                         "HTTP/1.1 404 Not Found\r\n\r\n"
                    )

               client_socket.sendall(response.encode())
          elif path.startswith('/echo/'):
               content_body = path.split("/")[2]
               response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    f"Content-Length: {len(content_body)}\r\n"
                    "\r\n"
                    f"{content_body}"
               )

               client_socket.sendall(response.encode())
          else:
               client_socket.send(notfound_response.encode())
          client_socket.close()
     finally:
          client_socket.close()
def start_server():
     host = 'localhost'
     port = 4221
     server_socket = socket.create_server((host, port), reuse_port=True)
     while True:
          client_socket , _ = server_socket.accept() # wait for client 
          thread = threading.Thread(target=handle_client,args=(client_socket,))          
          thread.start()
def main():
     # You can use print statements as follows for debugging, they'll be visible when running tests.
     print("Logs from your program will appear here!")
     start_server()
    
if __name__ == "__main__":
    main()

import socket  # noqa: F401
import threading
import os
import sys
import gzip
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
          
               directory = sys.argv[2]  if len(sys.argv) > 2 else ""
               filepath = f"{directory}{filename}"
               lines = data.decode().split("\r\n")
               for line in lines:
                    body = line
               file_existed_before = os.path.exists(filepath)
               os.makedirs(os.path.dirname(filepath), exist_ok=True)
               
               if data_header[0] == "POST":
                    with open(filepath, "w") as f:
                         f.write(body)
                    file_exists_now = os.path.exists(filepath)

                    if file_existed_before and file_exists_now:
                         with open(filepath,"r") as f:
                              file_content = f.read()
                         response = (
                              "HTTP/1.1 200 OK\r\n"
                              "Content-Type: application/octet-stream\r\n"
                              f"Content-Length: {len(file_content)}\r\n"
                              "\r\n"
                              f"{file_content}"
                         )
                    else: 
                         response = (
                              "HTTP/1.1 201 Created\r\n\r\n"
                         )                  
               else:  # GET request
                    if os.path.exists(filepath):
                         with open(filepath, "r") as f:
                              file_content = f.read()
                         response = (
                              "HTTP/1.1 200 OK\r\n"
                              "Content-Type: application/octet-stream\r\n"
                              f"Content-Length: {len(file_content)}\r\n"
                              "\r\n"
                              f"{file_content}"
                         )
                    else:
                         response = "HTTP/1.1 404 Not Found\r\n\r\n"

               client_socket.sendall(response.encode())
          elif path.startswith('/echo/'):
               content_body = path.split("/")[2]
               lines = data.decode().split("\r\n")
               matched = False
               for line in lines:
                    if line.startswith("Accept-Encoding"):
                         encoding_method =  line.split(":")[1].strip()
                         matched = True
                         break
               if matched:
                    compressed = gzip.compress(content_body.encode())
                    if encoding_method == 'gzip':
                         response = (
                              "HTTP/1.1 200 OK\r\n"
                              "Content-Type: text/plain\r\n"
                              "Content-Encoding: gzip\r\n"
                              "\r\n"
                              f"{compressed}"
                         )
                    else: 
                         response = (
                              "HTTP/1.1 200 OK\r\n"
                              "Content-Type: text/plain\r\n"
                              "\r\n"
                              f"{compressed}"
                         )
               else:
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

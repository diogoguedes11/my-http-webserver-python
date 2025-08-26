import socket  # noqa: F401

def start_server():
     host = 'localhost'
     port = 4221
     success_response = 'HTTP/1.1 200 OK\r\n\r\n'
     notfound_response = 'HTTP/1.1 404 Not Found\r\n\r\n'
     server_socket = socket.create_server((host, port), reuse_port=True)
     try:
          client_socket , _ = server_socket.accept() # wait for client 
          data = client_socket.recv(1024)
          print(f"Message Received: {data.decode()}")
          data_header = data.decode().split(" ")
          if len(data_header) > 1:
               path = data_header[1]
          else:
               path = ''
          if path == '/':
               client_socket.send(success_response.encode())
          if path == "/user-agent":
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
          if path.startswith('/echo/'):
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

def main():
     # You can use print statements as follows for debugging, they'll be visible when running tests.
     print("Logs from your program will appear here!")
     start_server()
    
if __name__ == "__main__":
    main()


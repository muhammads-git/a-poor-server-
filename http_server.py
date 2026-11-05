import socket
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# initialize a socket obj
so = socket.socket()
so.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
so.bind(('127.0.0.1',9000))
# listen means now the socket is looking for request, and ready to take requetst
so.listen()

# initialize pool
pool = ThreadPoolExecutor(max_workers=5)

# HANDLE CLIENT
def handle_client(conn):
   data = conn.recv(4096).decode()
   conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 32\r\n\r\nHello, this is Muhammads server.")
   print(data)
   conn.close()

while True:
   conn,addr = so.accept()
   # fire a THREAD
   # new_thread = threading.Thread(target=handle_client,args=(conn,))  # mulit-threading
   # new_thread.start()
   pool.submit(handle_client,conn)


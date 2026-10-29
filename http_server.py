import socket
import time
import threading


# initialize a socket obj
so = socket.socket()
so.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
so.bind(('127.0.0.1',9000))
# listen means now the socket is looking for request, and ready to take requetst
so.listen()

# HANDLE CLIENT
def handle_client(conn):
   data = conn.recv(4096).decode()
   conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 32\r\n\r\nHello, this is Muhammads server.")
   print(data)
   conn.close()

while True:
   conn,addr = so.accept()
   # fire a THREAD
   new_thread = threading.Thread(target=handle_client,args=(conn,))
   new_thread.start()


# we are now going to implement the threadpoolexecutor to limit the threads
# so to minimise cpu thrashing swapping and save its cyle

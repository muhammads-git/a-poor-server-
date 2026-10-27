import socket
import time
import threading

# s = threading.Thread()
# s.start()

# initialize a socket obj
so = socket.socket()

""" predict what this does:
   from the name seems like it sets the options, like what type of 
   socket connection it should be, 
   SOL_SOCKET: I guess, a sol socket could mean that, socket socket is sol
   SO_REUSEADDR: From re use addr i can predict that, the address it will be given,
   is the same addr used across the whole connection request/response
   """
so.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
""" bind: used for binding the address, like giving this connection a address where this 
will accept and talk.. a localhost IP , and a port like room where the connection is happening and requet
will be coming..."""

so.bind(('127.0.0.1',9000))

# listen means now the socket is looking for request, and ready to take requetst
so.listen()




# HANDLE CLIENT
def handle_client(conn):

   data = conn.recv(4096).decode()
   print(data)

   # conn.sendall()

   conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 32\r\n\r\nHello, this is Muhammads server.")

   
   conn.close()


while True:
   conn,addr = so.accept()
   new_thread = threading.Thread(target=handle_client,args=(conn,))
   new_thread.start()

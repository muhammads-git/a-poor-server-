import socket
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import selectors



# initialize a socket obj
so = socket.socket()
so.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
so.bind(('127.0.0.1',9000))
# listen means now the socket is looking for request, and ready to take requetst
so.listen(1000)


# set non-blocking
"""This tells OS something that, if no request or socket is connecting, dont stop
keep moving... dont freeze
"""
so.setblocking(False)

# inititaliz the demultiplexer classs
demultiplexer = selectors.DefaultSelector()

# HANDLE CLIENT
def handle_client(conn):
   try:
      conn.recv(4096).decode()
      conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 32\r\n\r\nHello, this is Muhammads server.")
      # print(f"Processed: {data.strip()}")
   except Exception as e:
      print(f'Error: {e}')
   finally:
      # unregister this client from demultiplexers, cause its done
      demultiplexer.unregister(conn)
      conn.close()


## a new function to accept new connections and handing to demultiplexerss
def accept_new_connections(listening_socket):
   conn, addr = listening_socket.accept()

   # set this client thread to non-blocking too
   conn.setblocking(False)

   # hand the conn to demultiplxer
   # tells OS "When this client sends DATA -> (EVENT_READ), call handle_client to handle"
   demultiplexer.register(conn,selectors.EVENT_READ,handle_client)

# Connect our main server socket to demultiplexer
# Tells OS "When a new client tries to connect call thiss"
demultiplexer.register(so,selectors.EVENT_READ,accept_new_connections)

print('Single-Threaded Event loop is initialized and spinning..')



while True:
   ready_events = demultiplexer.select()

   # now that kernel has handed you the tasks from demulitplexer lets see
   for key,mask in ready_events:
      callback = key.data # this gets the function call accept_new_connections or handle_client

      sock = key.fileobj # this gets the actual socket object

      callback(sock)  # runs the callback syncly on our main thread

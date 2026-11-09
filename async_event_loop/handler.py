
# import time
# from async_event_loop.configs import pool
# import socket 

# def handle_heavy_tasks(conn,data):
# #  """
# #    Yeh wo function hai jo pool ka background thread alag core par chalayega.
# #    Is ke andar time.sleep(2) ya heavy calc pure loop ko freeze nahi karegi.
# #    """
#     print(" -> [Worker Thread] Processing heavy 2-second job...")
#    #  time.sleep(2) # 2 Second delay simulation
    
#     # Send response back to the client directly from the worker thread
#     conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 32\r\n\r\nHello, this is Muhammads server.")
#     conn.close()
#     print(" -> [Worker Thread] Done! Response sent, socket closed.")


# def handle_client(conn): 
#    """ Main thread hands the client to new thread.. instead of handling itself and 
#    freezing, the whole server.. as tasks might take time to respond"""
#    from async_event_loop.main import demultiplexer 
#    try:
#       data = conn.recv(4096)
#       if data:
#          pool.submit(handle_heavy_tasks,conn,data)

#    except Exception as e:
#       print(f'Error inside client handler: {e}')
#       conn.close()



# def accept_new_connections(listening_socket,demultiplexer):
#    from async_event_loop.main import demultiplexer
#    conn, addr = listening_socket.accept()

#    #accept new conn without blockinggg broooo have million hands whateeverr
#    conn.setblocking(False)
#    demultiplexer.register(conn,1,handle_client)


import asyncio
import time
from async_event_loop.configs import thread_pool  # Bring in our capped pool

def heavy_blocking_db_query(data_payload):
    """
    The Indivisible 2-Second Block.
    This function runs COMPLETELY on a separate background thread core.
    """
    print(f" -> [Thread Pool] Worker thread running heavy 2-second job...")
    time.sleep(2)  # Simulating a heavy blocking database row processing
    return f"Processed: {data_payload.strip()}"

async def handle_client(reader, writer):
    """
    The Async Coroutine Handler.
    Processes socket stream buffers non-blockingly.
    """
    try:
        # Read from kernel buffer. If client is slow, the single thread yields instantly.
        raw_data = await reader.read(4096)
        if not raw_data:
            return
            
        data_string = raw_data.decode()

        # --- THE TRUE ASYNC DEFERRAL HAND-OFF ---
        # Grab the running event loop scheduling engine
        loop = asyncio.get_running_loop()
        
        # Tell the main thread: "Push this blocking work to the Thread Pool,
        # pause this specific context frame, and resume only when the worker thread drops the answer."
        result = await loop.run_in_executor(thread_pool, heavy_blocking_db_query, data_string)
        
        print(f" -> [Main Loop] Thread safely retrieved worker result: {result}")

        # Send response asynchronously back over the wire stream
        response = b"HTTP/1.1 200 OK\r\nContent-Length: 32\r\n\r\nHello, this is Muhammads server."
        writer.write(response)
        await writer.drain()  # Yield execution until the network hardware buffers clear out
        
    except Exception as e:
        print(f'Handler Error: {e}')
    finally:
        # Ensure the socket stream closes without causing leakage
        writer.close()
        await writer.wait_closed()


# ok it has still some issues while executing and handling requests but we will surely see it

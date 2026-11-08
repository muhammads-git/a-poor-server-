import socket
import asyncio
from async_event_loop.handler import handle_client  # Pull our clean client coroutine handler

async def main():
    # 1. Initialize native socket primitive
    so = socket.socket()
    so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    so.bind(('127.0.0.1', 9000))
    so.listen(1000)  # Give Windows Kernel a 1000-size handshake backlog buffer
    
    # 2. Strip blocking power so accept() can never block the execution line
    so.setblocking(False)

    # 3. Mount our socket inside asyncio's low-level multiplexer loop
    # This replaces your old manual loop and automatically boots up native select() loops
    server = await asyncio.start_server(handle_client, sock=so)
    
    print(" Muhammad's Architectural Async Multi-File Server is initialized!")
    print("   Main Thread handles non-blocking routing | Thread Pool processes CPU traps.")
    
    # Keep the multiplexer loop engine executing infinitely
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    # Start the engine tick at the OS level
    asyncio.run(main())

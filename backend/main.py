import asyncio

from backend.control.control_loop import ControlLoop
from backend.network.websocket_server import WebSocketServer


async def main():

    control_loop = ControlLoop()

    websocket_server = WebSocketServer()

    await asyncio.gather(
        control_loop.run(),
        websocket_server.run()
    )
    #asyncio.gather helps to runs both tasks concurrently, without it, one of the loops would run forever and otehr wont even start.


if __name__ == "__main__":
    asyncio.run(main())
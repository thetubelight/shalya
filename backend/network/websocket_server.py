from backend.shared_state import state_manager

import asyncio
import websockets


class WebSocketServer:

    async def handle_connection(self, websocket):
        print("Client connected")

        try:
            while True:

                state_json = state_manager.get_state().to_json()
                
                await websocket.send(state_json)

                await asyncio.sleep(0.05)

        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")

    async def run(self):

        server = await websockets.serve(
            self.handle_connection,
            "0.0.0.0",
            8765
        )

        print("WebSocket Server Running")

        await server.wait_closed()
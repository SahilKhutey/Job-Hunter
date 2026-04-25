import asyncio
import websockets
import json
import requests

def get_token():
    res = requests.post("http://localhost:8000/api/v1/auth/demo")
    return res.json()["access_token"]

async def test_ws():
    token = get_token()
    uri = f"ws://localhost:8000/ws?token={token}"
    async with websockets.connect(uri) as websocket:
        print("Connected!")
        greeting = await websocket.recv()
        print(f"Received: {greeting}")
        await websocket.send("ping")
        resp = await websocket.recv()
        print(f"Received: {resp}")

if __name__ == "__main__":
    asyncio.run(test_ws())

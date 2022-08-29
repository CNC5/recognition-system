import asyncio
import pathlib
import ssl
import websockets

async def wss_handler(websocket, path):
    data_chunk = await websocket.recv()

    print(f"data chunk recv: {data_chunk}")

    response = '0'
    await websocket.send(response)
    print(f"response: {response}")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
cert = pathlib.Path(__file__).with_name("cert.pem")
key = pathlib.Path(__file__).with_name("key.pem")
ssl_context.load_cert_chain(cert, keyfile=key)

start_server = websockets.serve(
    wss_handler, "localhost", 8765, ssl=ssl_context
)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

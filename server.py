import asyncio
import pathlib
import ssl
import websockets
import time
#import pyaudio
import wave
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--port", dest="port",
                    help="Change the port to serve on to PORT", metavar="PORT")
parser.add_argument("-d", "--dest", dest="host",
                    help="Change the address to serve on to HOST", metavar="HOST")

args = parser.parse_args()
if args.port:
    server_port = args.port
else:
    server_port = 8765
if args.host:
    server_addr = args.host
else:
    server_addr = 'localhost'
if args.port or args.host:
    print(f'Serving on {server_addr}:{server_port}')

async def wss_handler(websocket, path):
    chunk_count = 0
    data_chunk = ''
    rstart = time.localtime()
    sample_format = 8 #pyaudio.paInt16
    channels = 2
    fs = 44100

    print('handler start')
    filename = await websocket.recv()
    filename = 'server_' + filename
    await websocket.send('0')
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(2) #pyaudio.get_sample_size(sample_format)
    wf.setframerate(fs)
    while data_chunk != 'stop':
        data_chunk = await websocket.recv()
        print(f'data chunk {chunk_count} recv, size: {len(data_chunk)}\r', end='')
        await websocket.send('0')
        if data_chunk != 'stop':
            wf.writeframes(data_chunk)
        chunk_count += 1
    wf.close()
    print('\ngot sigstop from remote, handler stop')

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
cert = pathlib.Path(__file__).with_name("cert.pem")
key = pathlib.Path(__file__).with_name("key.pem")
ssl_context.load_cert_chain(cert, keyfile=key)

start_server = websockets.serve(
    wss_handler, server_addr, server_port, ssl=ssl_context
)

print('server start')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

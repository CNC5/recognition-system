import asyncio
import websockets
import time
import ssl
import pathlib
import pyaudio
import wave
import aioconsole
from argparse import ArgumentParser
import math
from ctypes import CFUNCTYPE, c_char_p, c_int, cdll
from contextlib import contextmanager

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

parser = ArgumentParser()
parser.add_argument("-d", "--dest", dest="host",
                    help="Change destination host to HOST", metavar="HOST")
parser.add_argument("-p", "--port", dest="port",
                    help="Change destination port to PORT", metavar="PORT")

args = parser.parse_args()

uri = 'wss://'
if args.host:
    uri += args.host
else:
    uri += 'localhost'
uri += ':'
if args.port:
    uri += args.port
else:
    uri += '8765'

if args.host or args.port:
    print(f'Sending to {uri}')

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
cert = pathlib.Path(__file__).with_name('cert.pem')
ssl_context.load_verify_locations(cert)


class bus_class:
    def __init__(self):
        self.run_flag = 1
        self.socket_cache = []
        self.file_cache = []
        self.socket_answer = None
        self.chunk_count = 0
        self.processed_chunk_count = 0
        self.sent_chunk_count = 0
        self.filename = ''
        self.rec_start = 0

bus = bus_class()
bus.rec_start = time.time()

chunk = 1024
sample_format = pyaudio.paInt16
channels = 2
fs = 44100
seconds = 3
with noalsaerr():
    audio_iface = pyaudio.PyAudio()
    stream = audio_iface.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)


def record_to_cache():
    while bus.run_flag:
        data = stream.read(chunk)
        bus.file_cache.append(data)
        bus.socket_cache.append(data)
        bus.chunk_count += 1

    stream.stop_stream()
    stream.close()
    audio_iface.terminate()

def write_to_file():
    rstart = time.localtime()
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    filename = f'record_{rstart.tm_hour}:{rstart.tm_min}:{rstart.tm_sec}_{rstart.tm_mday}.{rstart.tm_mon}.{rstart.tm_year}.wav'
    bus.filename = filename
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.get_sample_size(sample_format))
    wf.setframerate(fs)
    while bus.run_flag:
        if bus.file_cache:
            wf.writeframes(bus.file_cache.pop(0))
            bus.processed_chunk_count += 1
        else:
            time.sleep(0.1)
    wf.close()

def logger():
    while bus.run_flag:
        duration = time.time() - bus.rec_start
        time.sleep(0.1)
        print(f'Running, chunk: {bus.chunk_count},\
    processed: {bus.processed_chunk_count},\
    sent: {bus.sent_chunk_count},\
    file cache size: {len(bus.file_cache)},\
    socket cache size: {len(bus.socket_cache)},\
    started {math.floor(duration)} seconds ago \r',\
    end='')

async def send_to_socket():
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        await websocket.send(bus.filename)
        await websocket.recv()
        while bus.run_flag:
            if bus.socket_cache:
                sound_chunk = bus.socket_cache.pop(0)
                await websocket.send(sound_chunk)
                bus.socket_answer = await websocket.recv()
                bus.sent_chunk_count += 1
            else:
                await asyncio.sleep(0.1)
        await websocket.send('stop')
        answer = await websocket.recv()

async def record_in_thread():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, record_to_cache)

async def write_in_thread():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, write_to_file)

async def log_in_thread():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, logger)

async def breaker():
    await aioconsole.ainput()
    bus.run_flag = 0

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(record_in_thread(), write_in_thread(), log_in_thread(), send_to_socket(), breaker()))

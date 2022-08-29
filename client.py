loop = asyncio.get_event_loop()


class bus_class:
    def __init__(self):
        self.run_flag = 1
        self.socket_cache = None
        self.file_cache = None


bus = bus_class()

def read_audio_chunk():
    data = stream.read(chunk)
    file_cache.append(data)
    socket_cache.append(data)

def stop_audio_stream():
    stream.stop_stream()
    stream.close()
    audio_iface.terminate()

def write_audio_file():
    filename = f'{rstart.tm_sec}_{rstart.tm_min}_{rstart.tm_hour}_\
                {rstart.tm_mday}_{rstart.tm_mon}_{rstart.tm_year}_\
                record.wav'

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(stream.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(file_cache))
    wf.close()

def record_stream():
    rstart = time.localtime()
    while run_flag:
        read_audio_chunk()
    stop_audio_stream()
    rstop = time.localtime()
    write_audio_file()



def record_to_cache():



async def send_to_socket():



async def record_in_thread():
    await loop.run_in_executor(record_to_cache)

async def send_to_socket():
    await websocket.send(cache)

async def write_to_file():
    await aiofiles.open().write(cache)

async def main():
    await asyncio.gather(record_in_thread, send_to_socket, write_to_file)

asyncio.run(main())
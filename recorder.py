import pyaudio
import wave
import time
import asyncio
import aioconsole

chunk = 1024
sample_format = pyaudio.paInt16
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3

audio_iface = pyaudio.PyAudio()
stream = audio_iface.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

file_cache = []
socket_cache = []
run_flag = 1

async def breaker():
    await asyncio.sleep(0.01)
    tmp = await aioconsole.ainput('input')
    run_flag = 0
    print(f'stop: {run_flag}')

async def read_audio_chunk():
    data = stream.read(chunk)
    file_cache.append(data)
    socket_cache.append(data)

async def stop_audio_stream():
    stream.stop_stream()
    stream.close()
    audio_iface.terminate()
    print('stream stop')

async def write_audio_file():
    filename = f'{rstart.tm_sec}_{rstart.tm_min}_{rstart.tm_hour}_\
                {rstart.tm_mday}_{rstart.tm_mon}_{rstart.tm_year}_\
                record.wav'

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(stream.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(file_cache))
    wf.close()

async def record_stream():
    rstart = time.localtime()
    await asyncio.sleep(0.1)
    print('start')
    while run_flag:
        await asyncio.sleep(0.01)
        print('chunk')
        await read_audio_chunk()
    await stop_audio_stream()
    rstop = time.localtime()
    await write_audio_file()
    print('complete')

async def main():
    breaker_task = asyncio.ensure_future(breaker())
    stream_task = asyncio.ensure_future(record_stream())

    await breaker_task
    await stream_task


asyncio.run(main())


#breaker_future = asyncio.ensure_future(breaker())
#audio_stream_future = asyncio.ensure_future(record_stream())
#asyncio.get_event_loop().run_until_complete(breaker())
#audio_stream_future.terminate()

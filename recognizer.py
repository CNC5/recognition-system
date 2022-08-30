import speech_recognition as sr

r = sr.Recognizer()
record = sr.AudioFile('record_on_client.wav')
with record as source:
    r.adjust_for_ambient_noise(source)
    audio = r.record(source)

print(r.recognize_google(audio, language='ru'))
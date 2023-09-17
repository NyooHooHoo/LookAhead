import speech_recognition as sr
import wave
import pyaudio
from threading import Thread
import numpy as np
import time as t
import sounddevice as sd

r = sr.Recognizer()
p = pyaudio.PyAudio()

filename = "iris_recording.wav"
chunk = 1024
FORMAT = pyaudio.paInt16
channels = 1
sample_rate = 44100
record_seconds = 5
min_volume = 5  # 0.18
stream = p.open(format=FORMAT,
                channels=channels,
                rate=sample_rate,
                input=True,
                output=True,
                frames_per_buffer=chunk)

end = False
talking = False
soundframes = []
time_start_talk = 0

SHOW_INFO = False
SHOW_ERROR = False
SHOW_INPUT = True

text = ""

def info(message):
    if SHOW_INFO:
        print("[INFO]", message)


def error(message):
    if SHOW_ERROR:
        print("[ERROR]", message)


def inp(message):
    if SHOW_INPUT:
        print("[INPUT]", message)





def record():
    global soundframes

    info("starttalk")
    soundframes = []
    while talking:
        data = stream.read(chunk)

        soundframes.append(data)

    info('endtalk')
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(soundframes))


def format_seconds(secs):
    mins = int(secs / 60)
    secs = int(secs % 60)
    return str(mins) + " minutes and " + str(secs) + " seconds"


def update_talking(indata, outdata, frames, time, status):
    global talking, time_start_talk
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > min_volume:
        time_start_talk = t.time()
        if not talking:
            talking = True
            thread = Thread(target=record, args=[])
            thread.start()

    if volume_norm < min_volume and talking and t.time() - time_start_talk > 0.2:
        talking = False
        t.sleep(0.1)
        with sr.AudioFile(filename) as source:
            calculate(r.record(source))


def volume_input():
    print("started iris")
    with sd.Stream(callback=update_talking):
        while True:
            sd.sleep(1)
            if end:
                break


def calculate(audio_text):
    global end, text
    with sr.Microphone() as source:

        try:
            text = r.recognize_google(audio_text, language='en')
            inp(text)
            

        except sr.UnknownValueError:
            info("No speech detected.")


def get_text():
    return text


def set_text(new_thing):
    global text
    text = new_thing


def close():
    stream.stop_stream()
    stream.close()
    p.terminate()


def start():
    volume_input()


if __name__ == "__main__":
    volume_input()
    stream.stop_stream()
    stream.close()
    p.terminate()

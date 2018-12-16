import pyaudio
import math
import struct
import wave
import sys
import time
from messenger import send
import speech_recognition as sr

# Assuming Energy threshold upper than 30 dB
Threshold = 4

SHORT_NORMALIZE = (1.0 / 32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2
Max_Seconds_Listen = 60
Max_Seconds_Record = 3
TimeoutSignal = int((RATE / chunk * Max_Seconds_Listen) + 2)
TimeoutRecord = int((RATE / chunk * Max_Seconds_Record) + 2)
silence = True
FileNameTmp = 'audio/input.wav'
Time = 0
all_records = []


def GetStream(stream, chunk):
    return stream.read(chunk)


def rms(frame):
    count = len(frame) / swidth
    format = "%dh" % (count)
    shorts = struct.unpack(format, frame)

    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000


def send_on_messenger_trad(dest, dest_type):
    r = sr.Recognizer()
    file = sr.AudioFile(FileNameTmp)
    with file as source:
        audio = r.record(source)
        input_sentence = "Maurice n'a pas compris votre phrase."
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            input_sentence = r.recognize_google(audio, language="fr-FR")

        except sr.UnknownValueError:
            print("Google Speech Recognition n'a pas pu comprendre votre phrase")
        except sr.RequestError as e:
            print(
                "Problèmes lors de la réception du résultat de la requête de Google Speech Recognition service; {0}".format(
                    e))
    send(FileNameTmp, input_sentence, dest, dest_type)


def send_on_messenger(dest, dest_type):
    send(FileNameTmp, "", dest, dest_type)


def WriteSpeech(p, stream, WriteData, dest, dest_type):
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(FileNameTmp, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(WriteData)
    wf.close()
    send_on_messenger(dest, dest_type)


def KeepRecord(p, stream, TimeoutSignal, LastBlock, dest, dest_type):
    global all_records
    all_records.append(LastBlock)
    start_time = time.time()
#    while time.time() - start_time < Max_Seconds:
    for i in range(TimeoutRecord):
        try:
            data = GetStream(stream, chunk)
        except Exception as e:
            print(e)
            continue
        # I change here (new Ident)
        all_records.append(data)

    print("end record after timeout")
    data = b''.join(all_records)
    print("write to File")
    WriteSpeech(p, stream, data, dest, dest_type)
    silence = True
    Time = 0
    all_records = []
    listen(silence, Time, dest, dest_type)


def listen(silence, Time, dest, dest_type):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    print("waiting for Speech")
    while silence:
        try:
            input = GetStream(stream, chunk)
        except Exception as e:
            print(e)
            continue
        rms_value = rms(input)
        print(rms_value)
        if (rms_value > Threshold):
            silence = False
            LastBlock = input
            print("hello ederwander I'm Recording....")
            KeepRecord(p, stream, TimeoutSignal, LastBlock, dest, dest_type)
        Time = Time + 1
        if (Time > TimeoutSignal):
            print("Time Out No Speech Detected")
            sys.exit()


# listen(silence, Time, "100005420857065", "user")
listen(silence, Time, "1938896156193853", "group")

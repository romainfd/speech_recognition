import snowboydecoder
import sys
import signal
import speech_recognition as sr
import os
import sounddevice as sd
import pyaudio
import wave

listening_interrupted = False


def audioRecorderCallbackDefault(fname):
    os.system("afplay audio/Deadbolt_Lock.mp3 -v 5")
    print("converting audio to text from " + fname)
    r = sr.Recognizer()
    with sr.AudioFile(fname) as source:
        audio = r.record(source, duration=2)  # read the entire audio file
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("You said: " + r.recognize_google(audio, language="fr-FR"))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # os.remove(fname)


def detectedCallback():
    os.system("afplay audio/Deadbolt_Lock.mp3 -v 5")
    print('recording audio... ', end='', flush=True)


def interruptCallback():
    global listening_interrupted
    return listening_interrupted


def record_input(callback):
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 3

    p = pyaudio.PyAudio()

    os.system("afplay audio/Deadbolt_Lock.mp3 -v 5")
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    print("* recording")
    all_records = []
    for i in range(0, int(44100 / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)
        all_records.append(data)
        # check for silence here by comparing the level with 0 (or some threshold) for
        # the contents of data.
        # then write data or not to a file
    complete_data = b''.join(all_records)
    wf = wave.open("input.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(complete_data)
    wf.close()
    print("* done")
    stream.stop_stream()
    stream.close()
    p.terminate()
    callback("input.wav")


def listen(hotword_model="jarvis.pmdl",
           audio_recorder_callback_param=audioRecorderCallbackDefault,
           duration=5,
           sensitivity=0.45):
    def signal_handler(signal, frame):
        # Instead of interrupt, we launch the recognition
        # global listening_interrupted
        # listening_interrupted = True
        record_input(audio_recorder_callback_param)

    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder.HotwordDetector(hotword_model, sensitivity=sensitivity, audio_gain=1)
    print('Listening... Press Ctrl+C to exit')

    # main loop
    detector.start(detected_callback=detectedCallback,
                   audio_recorder_callback=audio_recorder_callback_param,
                   interrupt_check=interruptCallback,
                   sleep_time=0.01,
                   recording_timeout=duration)

    detector.terminate()


if __name__ == "__main__":
    listen()

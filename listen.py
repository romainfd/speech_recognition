import snowboydecoder
import sys
import signal
import speech_recognition as sr
import os

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
        print("You said: "+r.recognize_google(audio, language="fr-FR"))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # os.remove(fname)


def detectedCallback():
    os.system("afplay audio/Deadbolt_Lock.mp3 -v 5")
    print('recording audio... ', end='', flush=True)


def signal_handler(signal, frame):
    global listening_interrupted
    listening_interrupted = True


def interruptCallback():
    global listening_interrupted
    return listening_interrupted


def listen(hotword_model="jarvis.pmdl",
           audio_recorder_callback_param=audioRecorderCallbackDefault,
           duration=5,
           sensitivity=0.5):

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

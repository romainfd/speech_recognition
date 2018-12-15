import speech_recognition as sr

# Record Audio
r = sr.Recognizer()


def listen_to_input(callback, duration=2):
    """ Launches the microphone to listen for duration seconds and then call callback(input_sentence) """
    with sr.Microphone() as source:
        print("Nous vous écontons:")
        audio = r.listen(source, phrase_time_limit=duration)

    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        input_sentence = r.recognize_google(audio, language="fr-FR")
        print("You said: " + input_sentence)
        callback(input_sentence)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

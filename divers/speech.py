import speech_recognition as sr
from talk import talk



def listen_to_input(callback=None, duration=2):
    # Record Audio
    r = sr.Recognizer()

    """ Launches the microphone to listen for duration seconds and then call callback(input_sentence) """
    with sr.Microphone() as source:
        # talk("Nous calibrons notre micro avec le son ambiant. Patientez 1 seconde.")
        # r.adjust_for_ambient_noise(source)
        print("Nous vous écontons:")
        audio = r.listen(source, phrase_time_limit=duration)

    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        input_sentence = r.recognize_google(audio, language="fr-FR")
        print("You said: " + input_sentence)
        if callable(callback):
            callback(input_sentence)

    except sr.UnknownValueError:
        print("Google Speech Recognition n'a pas pu comprendre votre phrase")
    except sr.RequestError as e:
        print("Problèmes lors de la réception du résultat de la requête de Google Speech Recognition service; {0}".format(e))


if __name__ == "__main__":
    while True:
        listen_to_input(duration=2)

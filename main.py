from levenshtein import distance
from talk import talk
from listen import listen
import numpy as np
import os
import speech_recognition as sr

duration = 5

cmds = [{
    "name": "appel",
    "action": lambda input_list: "Bien reçu, j'appelle {}".format("".join(input_list[1:]))
}, {
    "name": "alert",
    "action": lambda input_list: "Bien reçu, je mets une alerte ici sur {}".format("".join(input_list[1:]))
}, {
    "name": "infos",
    "action": lambda input_list: "Bien reçu, voilà les infos {}".format("".join(input_list[1:]))
}]

# ex:
#   Appelle mes parents
#   Alerte trou de neige
#   Infos météo (ou traffic)


def audioRecorderCallback(fname):
    os.system("afplay audio/Deadbolt_Lock.mp3 -v 5")
    print("Conversion de l'audio depuis " + fname)
    r = sr.Recognizer()
    with sr.AudioFile(fname) as source:
        audio = r.record(source, duration=duration)  # read the entire audio file
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        input_sentence = r.recognize_google(audio, language="fr-FR")
        print("Vous avez dit: " + input_sentence)

        # On appelle la suite
        act_on_input(input_sentence)

    except sr.UnknownValueError:
        print("Google Speech Recognition n'a pas pu comprendre votre phrase")
    except sr.RequestError as e:
        print(
            "Problèmes lors de la réception du résultat de la requête de Google Speech Recognition service; {0}".format(
                e))
    try:
        os.remove(fname)
    except FileNotFoundError:
        pass


def do_input(input_str):
    input_list = input_str.split()
    cmd = input_list[0]
    distances = [distance(cmd, registered_cmd["name"]) for registered_cmd in cmds]
    argmin = np.argmin(distances)
    return cmds[argmin]["action"](input_list)


def act_on_input(input_str):
    answer = do_input(input_str)
    talk(answer)


if __name__ == "__main__":
    # listen_to_input(act_on_input, duration=2)
    # act_on_input("Appelle mes parents")
    # act_on_input("Infos temps d'attente")
    # act_on_input("Alert trou de glace")

    listen(duration=duration, audio_recorder_callback_param=audioRecorderCallback)

from levenshtein import distance
from talk import talk
from listen import listen
import numpy as np
import os
import speech_recognition as sr
import requests
from googletrans import Translator
import subprocess


duration = 10
global call_process


def infos_handler(input_list):
    def get_meteo():
        r = requests.get(
            "https://samples.openweathermap.org/data/2.5/weather?q=london&appid=b6907d289e10d714a6e88b30761fae22")
        if r.status_code != 200:
            return "Impossible de se connecter au service de météo."
        meteo_en = r.json()["weather"][0]["description"]
        translator = Translator()
        meteo = translator.translate(text=meteo_en, dest='fr').text
        return meteo

    def get_trafic():
        return "Le trafic est dégagé sur l'ensemble de la station."

    infos_cmds = [{
            "name": "météo",
            "action": lambda: "Bien reçu, voici les infos météo actuelles de la Plagne. {}".format(get_meteo())
        }, {
            "name": "trafic",
            "action": lambda: "Bien reçu, voici les infos trafic. {}".format(get_trafic())
        }]
    distances = [distance(input_list[1], registered_cmd["name"]) for registered_cmd in infos_cmds]
    return infos_cmds[np.argmin(distances)]["action"]()


def join_handler(input_list):
    global call_process
    call_process = subprocess.Popen(['python', 'divers/record.py'])
    print('Running in process', call_process.pid)
    return "Bien reçu, tu as rejoins le groupe 'Potos du ski'."


def quit_handler(input_list):
    global call_process
    call_process.kill()
    print("Sous-process fini: tu as quitté la conversation.")
    return "Bien reçu, tu as quitté le groupe 'Potos du ski'."


def route_handler(input_list):
    def get_route(input_list):
        guide_cmds = [{
            "name": "sommet",
            "action": lambda: "Bien reçu, pour rejoindre le sommet le plus rapidement possibme: "
                              "prendre la piste bleue 'Promenade' puis prendre avec le télésiège"
        }, {
            "name": "station",
            "action": lambda: "Bien reçu, pour rejoindre la station le plus rapidement possible: "
                              "prendre la piste rouge 'Traversée'"
        }]
        distances = [distance(input_list[2], registered_cmd["name"]) for registered_cmd in guide_cmds]
        return guide_cmds[np.argmin(distances)]["action"]()

    route_cmds = [{
            "name": "idéal",
            "action": lambda input_list: "Bien reçu, le trajet avec le moins d'attente pour le moment est: {}".format(
                "Descendre la piste rouge 'Chamois', prendre le télésiège et redescendre de l'autre côté du sommet"
            )
        }, {
            "name": "vers",
            "action": get_route
        }]
    if len(input_list) < 2:
        cmd_index = 0  # idéal
    else:
        distances = [distance(input_list[1], registered_cmd["name"]) for registered_cmd in route_cmds]
        cmd_index = np.argmin(distances)
    return route_cmds[cmd_index]["action"](input_list)


cmds = [{
        "name": "appel",
        "action": lambda input_list: "Bien reçu, j'appelle {}".format("".join(input_list[1:]))
    }, {
        "name": "alert",
        "action": lambda input_list: "Bien reçu, je mets une alerte ici sur {}".format("".join(input_list[1:]))
    }, {
        "name": "infos",
        "action": lambda input_list: infos_handler(input_list)
    }, {
        "name": "aide",
        "action": lambda input_list: "Bien reçu, j'ai transmis tes coordonnées GPS à la station. "
                                     "Je te mets en contact avec les urgences."
    }, {
        "name": "rejoins",
        "action": lambda input_list: join_handler(input_list)
    }, {
        "name": "raccroche",
        "action": lambda input_list: quit_handler(input_list)
    }, {
        "name": "trajet",
        "action": lambda input_list: route_handler(input_list)
}]


# ex:
#   Appelle mes parents
#   Alerte trou de neige
#   Infos météo (ou trafic)
#   Aide
#   Rejoins 'Potos du ski'
#   Raccroche
#   Trajet idéal
#   Trajet vers station (ou sommet) rapidement
#   -- Trajet vers Thomas


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
    if distances[argmin] > 3:
        return "Désolé, je n'ai pas compris votre requete."
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

# Speech Recognition system for a ski assistant
The 'Maurice' ski assistant lets you talk with your friends and get information about the station (traffic, weather, waiting time, alerts, ...) without taking. your gloves off or having to get your phone out of your jacket. To do so, it uses a Speech Recognition and Talker based on Google products to interact with all the apps functionalities.

## To install the dependencies:
* run `make dep` on the root of the project
* if you have an error with PyAudio dep missing, follow the guide [here](https://pypi.org/project/SpeechRecognition/#pyaudio-for-microphone-users)

## To run the speech recognition:
* run `python divers/speech.py`
* it will record for 2 seconds

## To run the complete interface (speech recognition, actions and answers said back):
* run `make`
* Set your volume to be sure to hear the answers
* Make sure your microphone is connected
* You can use "Ctrl + C" or say "Jarvis" to launch the voice recognition system
* Here are the different functionalities:
    * Say `rejoindre Potos du ski` to join the group "Potos du ski"
        * Then, whenever you speak loud enough, this would be send the audio message to your friends
        * Say `raccroche` to stop the call with your group of friends
    * Say `infos météo` => live weather from London
    * Say `infos trafic` => live traffic of the ski resort
    * Say `aide` => sends your GPS coordinates and calls the emergency service
    * Say `appelle mes parents` => to call your parents if you're lost
    * Say `alerte trou de neige` => to indicate to the app there is a hole in the ground. 
        This will warn the other users when they arrive on the spot.
    * Say `trajet idéal` => to have the itinerary with the less waiting time (for button lifts and ski lifts)
    * Say `trajet vers sommet (ou station)` => to have the fastest path to the summit or the station
    
    

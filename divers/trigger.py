# HAS TO BE ON THE ROOT TO WORK

import snowboydecoder

hotword = "jarvis"


def detected_callback():
    print("hotword detected")


detector = snowboydecoder.HotwordDetector(hotword + ".pmdl", sensitivity=0.6, audio_gain=1)
print("Listening to " + hotword)
detector.start(detected_callback)

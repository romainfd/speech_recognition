# Import the required module for text
# to speech conversion
from gtts import gTTS
from gtts.tokenizer import pre_processors
import gtts.tokenizer.symbols

# This module is imported so that we can
# play the converted audio
import os

# The text that you want to convert to audio
# my_text = 'Bienvenue Romain!'

gtts.tokenizer.symbols.SUB_PAIRS.extend([
    ('mes', 'té'),
    ('mon', 'ton'),
    ('ma', 'ta')
])


def talk(text):
    # we preprocess the word to change the words
    new_text = pre_processors.word_sub(text)

    # Language in which you want to convert
    language = 'fr'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    my_obj = gTTS(text=new_text, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome
    my_obj.save("audio/cmd.mp3")

    # Playing the converted file
    os.system("afplay audio/cmd.mp3")

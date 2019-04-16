import tempfile
import os
from os import mkdir, path
import pygame
import pyttsx3

from requests.exceptions import HTTPError
from pygame import mixer
CLIENT_DIR =    path.dirname(path.abspath(__file__))
DATA_DIR =      path.join(CLIENT_DIR, 'data')
def init():
    """ Initialize the pygame mixer """
    mixer.init()

def play_mp3(file_name, file_path=path.join(DATA_DIR,   'media'), blocking=False):
    """Plays a local MP3 file

    :param file_name: top-level file name (e.g. hello.mp3)
    :param file_path: directory containing file ('media' folder by default)
    :param blocking: if false, play mp3 in background
    """
    if ".mp3" in file_name:
        mixer.music.load(os.path.join(file_path, file_name))
        mixer.music.play()
    else:
        sound = pygame.mixer.Sound(os.path.join(file_path, file_name))
        chan = pygame.mixer.find_channel()
        chan.queue(sound)

    if blocking:
        while mixer.music.get_busy():
            pygame.time.delay(100)


def TalkToMe(phrase, cache=False, filename='default', show_text=True, log_text=True):
    """Speaks a given text phrase

    :param phrase: text string to speak
    :param cache: if True, store .mp3 in 'media/responses'
    :param filename: filename if cached
    :param show_text: if True, store .mp3 in 'media/responses'
    :param cache: if True, store .mp3 in 'media/responses'
    """
    
    try:
        phrase = phrase[:140]
        for line in phrase.splitlines():
            print("Phoenix : %s" %phrase)
    #offline
        engine = pyttsx3.init()
        engine.say(phrase)
        engine.runAndWait()
        '''
        if not cache:
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.mp3',delete=False) as f:
                (temp_path, temp_name) = os.path.split(f.name)
            play_mp3(temp_name, temp_path)
            os.remove(os.path.join(temp_path, temp_name))
        else:
            tts.save(filename)
            print('Saved to: '+filename)
            '''
    except HTTPError as e:
        print("Sphinx probably wrong")

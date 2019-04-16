import pyaudio
import traceback
import os
from os import mkdir, path
from os.path import join
import sys
from sys import platform as _platform
import speech_recognition as sr
import logging
from gtts import gTTS
from pocketsphinx import DefaultConfig, Decoder, get_model_path, get_data_path, LiveSpeech
import tts

def ignore_stderr():
    """ Ignore unwanted 'error' output from pyglet/pyaudio """
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)
        
def init():
    CLIENT_DIR = path.dirname(path.abspath(__file__))
    BASE_DIR =   path.dirname(CLIENT_DIR)
    DATA_DIR = path.join(CLIENT_DIR, 'data')
    LOGS_DIR = path.join(DATA_DIR, 'logs')
    MEDIA_DIR = path.join(DATA_DIR, 'media')
    INPUTS_DIR = path.join(MEDIA_DIR, 'iexample_inputs')
    RESPONSES_DIR = path.join(MEDIA_DIR, 'responses')
    USERS_DIR = path.join(DATA_DIR, 'users')

    LOG_NAME = 'phoenix'
    LOG_FILE = path.join(LOGS_DIR, LOG_NAME+'.log')
    LOG_LEVEL = logging.DEBUG

    
    SR_DIR = path.dirname(path.abspath(sr.__file__))
    MODELDIR = "C:\Python27\Lib\site-packages\pocketsphinx\model"
                #linux = /usr/local/share/pocketsphinx
    DIRS = [LOGS_DIR, MEDIA_DIR, INPUTS_DIR, RESPONSES_DIR, USERS_DIR]
    for d in DIRS:
        if not path.exists(d):
            mkdir(d)
            
    config = DefaultConfig()
    config.set_string('-hmm', os.path.join(MODELDIR, 'en-us'))
    config.set_string('-lm', os.path.join(MODELDIR,'en-us.lm.bin'))#en-us.lm.bin 5921.lm.bin
    config.set_string('-dict', os.path.join(MODELDIR, 'cmudict-en-us.dict'))#cmudict-en-us.dict 5921.dict
    config.set_string('-kws', os.path.join(MODELDIR, 'keyphrase.txt'))

    global decoder, p

    decoder = Decoder(config)
    p = pyaudio.PyAudio()

    global r
    r = sr.Recognizer()

def listen_keyword():
    ''' Passively listens for keyword '''
    #with ignore_stderr():
    global decoder, p
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                    input=True, frames_per_buffer=1024)
    stream.start_stream()

    #print("Waiting to be woken up...")
    # Process audio chunk by chunk. On keyword detected perform action and restart search
    decoder.start_utt()
    waiting = False
    wait_count = 0
    while True:
        buf = stream.read(1024, exception_on_overflow=False)
        decoder.process_raw(buf, False, False)
        if decoder.hyp():
            if decoder.hyp().hypstr[:13] == "phoenix cancel" or decoder.hyp().hypstr[:11] == "phoenix stop":
                decoder.end_utt()
                return "phoenix stop"
            else:
                if waiting:
                    if wait_count >= 8:
                        decoder.end_utt()
                        return "phoenix"
                    else:
                        wait_count += 1
                else:
                    waiting = True
def MyCommand():
    global r
    #with ignore_stderr():
    with sr.Microphone() as src:
        r.adjust_for_ambient_noise(src)
        print("Now listening...")
        tts.play_mp3('double-beep.mp3')
        audio = r.listen(src)

    command = ""        
    try :
        command = r.recognize_google(audio, language='en-US')
        print("\nYou said: %s\n"%command)
    except r.UnknownValueError:
        print("Your last command could not be heard")
        tts.TalkToMe("I could not hear you")
        command = MyCommand()
    finally:
        return command

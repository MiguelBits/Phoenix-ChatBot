from __future__ import print_function

import traceback
import os
import re
import yaml
import smtplib
import tts, stt
import sys
import skills

inst = None

try:
    input = raw_input  # Python 2 fix
except NameError:
    pass


def init():
    global inst
    inst = Brain()
class Brain:
    def __init__(self, greet_user=True):
        if greet_user:
            self.greet()
        stt.init()
        tts.init()

        self.quit_flag = False

    def greet(self):
        """ Greet the user """
        print('\n~ Hello, what can I do for you today?\n')
        print('~ Try asking:')
        print('  - "Phoenix (double beep) how are you doing"')
        print('  - "Phoenix (double beep) repeat"')
        print('  - "Phoenix (double beep) open facebook.com"\n')

    def execute_tasks(self, mod, text):
        """ Executes a module's task queue """
        for task in mod.task_queue:
            task.action(text)
            if task.greedy:
                break
         
            
    def run(self):
        """ Listen for input, match the modules and respond """
        while True:
            print("Waiting to be woken up..")
            keyword = stt.MyCommand()
            wakeupword = ("phoenix", "Phoenix")
            for i in wakeupword:
                if i in keyword:
                    tts.play_mp3("double-beep.wav")
                    tts.TalkToMe("System Online")
                    execution(keyword)
                    
                
def execution(phrase):
    if len(phrase.split()) < 3 :
        print("Active Listening mode activated !")
        while True:
            command = stt.MyCommand()
            skills.intent(command)
    if len(phrase.split()) >= 3:
        print("Active Listening mode activated !")
        while True:
            skills.intent(phrase)
            command = stt.MyCommand()
            skills.intent(command)

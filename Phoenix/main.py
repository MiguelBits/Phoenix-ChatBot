""" Hey Phoenix start script """

import sys
from os import path
import stt, tts
# Add "phoenix" to python's path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import brain

brain.init()
brain.inst.run()

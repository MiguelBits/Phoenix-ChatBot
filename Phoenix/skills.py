import tts, stt
import weatherpy
import singpy


def intent(phrase):
    ''' Identifies the intent in the given command'''
    if "weather" in phrase:
        weatherpy.intent(phrase)
    elif "sing" in phrase:
        print("singing mode")
        singpy.intent(phrase)
    else:
        print("--  That is not a command --")

    

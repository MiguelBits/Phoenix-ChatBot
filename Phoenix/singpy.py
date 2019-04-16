import tts, stt
import spacy
import en_core_web_sm
from PyLyrics import *


def intent(phrase):
    '''Sing command'''
    nlp = en_core_web_sm.load()
    dicta = {"singer":0}
    nlp_sing = nlp(u"%s"%phrase)
    array_list = [(i, i.label_, i.label) for i in nlp_sing.ents]
    array_array = ([[item] for c_list in array_list for item in c_list])
    iden_list = ("[u'GPE']", "[u'WORK_OF_ART']", "[u'PERSON']","[u'ORG']")
    num = 0
    try :
        for s in array_array:
            num = num + 1
            singer = s
            dicta[str(s)] = str(num)
            for i in iden_list:
                if str(s) == str(i):
                    iden = dicta[str(s)]
                    idennum = int(iden) - 1
                    break
            for key in dicta.keys():
                if dicta[key] == str(idennum):
                    singer = key
                    singer = singer.replace("[", "")
                    singer = singer.replace("]", "")
                    
                    print(dicta[key] + singer)
                    
                    new_array_array = array_array.replace(str(dicta[key]), " ")
                    new_array_array = new_array_array.replace(str(key), " ")
                            
            for s in new_array_array:
                num = num + 1
                song = s
                dicta[str(s)] = str(num)
                for i in iden_list:
                    if str(s) == str(i):
                        iden = dicta[str(s)]
                        idennum = int(iden) - 1
                        break
            for key in dicta.keys():
                if dicta[key] == str(idennum):
                    song = key
                    song = song.replace("[", "")
                    song = song.replace("]", "")
                    
                    print(dicta[key] + song)
                    
        tts.TalkToMe(str(PyLyrics.getLyrics("%s"%singer,"%s"%song)))
    except:
        try:
            for s in array_array:
                song = s
                dicta[str(s)] = str(num)
                for i in iden_list:
                    if str(s) == str(i):
                        iden = dicta[str(s)]
                        idennum = int(iden) - 1
                        break
            for key in dicta.keys():
                if dicta[key] == str(idennum):
                    song = key
                    song = song.replace("[", "")
                    song = song.replace("]", "")

                    print(dicta[key] + song)
                    
                    new_array_array = array_array.replace(str(dicta[key]), " ")
                    new_array_array = new_array_array.replace(str(key), " ")
                            
            for s in new_array_array:
                singer = s
                dicta[str(s)] = str(num)
                for i in iden_list:
                    if str(s) == str(i):
                        iden = dicta[str(s)]
                        idennum = int(iden) - 1
                        break
            for key in dicta.keys():
                if dicta[key] == str(idennum):
                    singer = key
                    singer = song.replace("[", "")
                    singer = song.replace("]", "")
                    
                    print(dicta[key] + singer)
                    
            
            tts.TalkToMe(str(PyLyrics.getLyrics("%s"%singer,"%s"%song)))
        except:
            tts.TalkToMe(" I could not find that song, let's go through it slowly")
            tts.TalkToMe("Tell me only who is the song's artist")
            singer = stt.MyCommand()
            tts.TalkToMe("Now give me just the song's name")
            song = stt.MyCommand()
            tts.TalkToMe(str(PyLyrics.getLyrics("%s"%singer,"%s"%song)))

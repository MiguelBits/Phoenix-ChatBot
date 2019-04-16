import tts, stt
import spacy
import en_core_web_sm
from weather import Weather, Unit


def intent(phrase):
    ''' Weather command'''
    cityExists = False
    nlp = en_core_web_sm.load()
    phrase = phrase.replace("Phoenix","phoenix")
    num = 0
    nlp_weather = nlp(u"%s"%phrase)
    w_array_list = [(i, i.label_, i.label) for i in nlp_weather.ents]
    w_array_array = ([[item] for c_list in w_array_list for item in c_list])
    dicta = {"city": 0}
    day = 0
    today = ("tomorrow", "today", "now", "this day")
    
    for i in today:
        if i in phrase:
            day = 4
    if ("tomorrow") in phrase:
        day = 3
    if ("two days") in phrase:
        day = 2
    if ("three days") in phrase:
        day = 1
    
    try:
        for c in w_array_array:
            num = num +1
            dicta[str(c)] = str(num)
            if str(c) == str([u'GPE']):
                ugpe = dicta["[u'GPE']"]
                citynum = int(ugpe) - 1
                for key in dicta.keys():
                    if dicta[key] == str(citynum):
                        city = key
                        city = city.replace("[", "")
                        city = city.replace("]", "")
                break
        weather = Weather(unit=Unit.CELSIUS)
        location = weather.lookup_by_location('%s'%city)
        forecasts = location.forecast
        tts.TalkToMe("We are")
        for forecast in forecasts:
            tts.TalkToMe("On the %s, It is %s, With a maximum of %s Celsius' Degrees And a low of %s Celsius' Degrees"%(forecast.date,forecast.text,forecast.high,forecast.low))
            day = day + 1
            if day == 5:
                break
        print("Done!")
    except: 
        while cityExists == False:
            try:
                tts.TalkToMe("Now tell me only the city please")
                command = "in "
                command = command + stt.MyCommand()
                num = 0
                nlp_weather = nlp(u"%s"%command)
                w_array_list = [(i, i.label_, i.label) for i in nlp_weather.ents]
                w_array_array = ([[item] for c_list in w_array_list for item in c_list])
                dicta = {"city": 0}
                for c in w_array_array:
                    num = num +1
                    dicta[str(c)] = str(num)
                    if str(c) == str([u'GPE']):
                        ugpe = dicta["[u'GPE']"]
                        citynum = int(ugpe) - 1
                        for key in dicta.keys():
                            if dicta[key] == str(citynum):
                                city = key
                                city = city.replace("[", "")
                                city = city.replace("]", "")

                weather = Weather(unit=Unit.CELSIUS)
                location = weather.lookup_by_location('%s'%city)
                forecasts = location.forecast
                tts.TalkToMe("We are")
                for forecast in forecasts:
                    day = day + 1
                    tts.TalkToMe("On the %s, It is %s, With a maximum of %s Celsius' Degrees And a low of %s Celsius' Degrees"%(forecast.date,forecast.text,forecast.high,forecast.low))
                    if day == 5:
                        cityExists = True
                        break
                print("Done!")
            except:
                tts.TalkToMe("I did not find that city, give me only the city again")
                city = stt.MyCommand()
                weather = Weather(unit=Unit.CELSIUS)
                location = weather.lookup_by_location('%s'%city)
                forecasts = location.forecast
                tts.TalkToMe("We are")
                for forecast in forecasts:
                    day = day + 1 
                    tts.TalkToMe("On the %s, It is %s, With a maximum of %s Celsius' Degrees And a low of %s Celsius' Degrees"%(forecast.date,forecast.text,forecast.high,forecast.low))
                    if day == 5:
                        cityExists = True
                        break
                print("Done!")


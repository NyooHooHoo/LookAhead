import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    selected_voice = voices[1].id  

    engine.setProperty('rate', 150)

    engine.setProperty('voice', selected_voice)
    engine.say(text)
    engine.runAndWait()
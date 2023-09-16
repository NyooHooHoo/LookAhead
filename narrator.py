import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    selected_voice = voices[0].id  

    engine.setProperty('rate', 150)

    engine.setProperty('voice', selected_voice)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    input_text = input("Enter the text you want to convert to speech: ")
    text_to_speech(input_text)
import speech_recognition as sr
import pygame

name = "iris"

def play_wav_file(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def listen_and_record():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        with microphone as source:
            print(f"Listening for {name}... Say {name} to start recording.")
            audio = recognizer.listen(source)

        try:
            # Recognize the keyword
            keyword = recognizer.recognize_google(audio)
            if name in keyword.lower():
                print(f"Keyword {name} detected. Recording...")

                play_wav_file("iris_sound.wav")

                # Listen for a single sentence
                with microphone as source:
                    audio = recognizer.listen(source, phrase_time_limit=5)

                try:
                    # Recognize speech
                    sentence = recognizer.recognize_google(audio)
                    print("You said:", sentence)
                except sr.UnknownValueError:
                    print("Couldn't understand the sentence. Please try again.")
                    recognizer = sr.Recognizer()

            else:
                print(f"Keyword not detected. Please say {name}.")

            recognizer = sr.Recognizer()

        except sr.UnknownValueError:
            print("Couldn't understand the keyword. Please try again.")
            recognizer = sr.Recognizer()

if __name__ == "__main__":
    listen_and_record()
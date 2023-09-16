import speech_recognition as sr

def listen_and_record():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        with microphone as source:
            print("Listening for 'hello'... Say 'hello' to start recording.")
            audio = recognizer.listen(source)

        try:
            # Recognize the keyword
            keyword = recognizer.recognize_google(audio)
            if "hello" in keyword.lower():
                print("Keyword 'hello' detected. Recording...")

                # Listen for a single sentence
                with microphone as source:
                    audio = recognizer.listen(source, phrase_time_limit=5)

                try:
                    # Recognize speech
                    sentence = recognizer.recognize_google(audio)
                    print("You said:", sentence)
                except sr.UnknownValueError:
                    print("Couldn't understand the sentence. Please try again.")

            else:
                print("Keyword not detected. Please say 'hello'.")

            recognizer = sr.Recognizer()

        except sr.UnknownValueError:
            print("Couldn't understand the keyword. Please try again.")

if __name__ == "__main__":
    listen_and_record()

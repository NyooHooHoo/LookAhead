import speech_recognition as sr

# Function to play a beep sound
def play_beep():
    duration = 0.2  # Duration of the beep in seconds
    frequency = 1000  # Frequency of the beep in Hz
    sample_rate = 44100  # Sample rate for audio playback

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    sd.play(audio_data, sample_rate)
    sd.wait()

# Function to listen for the keyword "test" and record the sentence
def listen_and_record():
    recognizer = sr.Recognizer()

    while True:
        microphone = sr.Microphone()
        print("Listening for 'hello'...")

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_sphinx(audio)
            print(f"Recognized: {text}")

            if "hello" in text.lower():
                print("Keyword 'hello' detected!")
                play_beep()  # Play the beep sound

                print("Listening for a sentence...")
                with microphone as source:
                    recognizer.adjust_for_ambient_noise(source, duration=2)
                    audio = recognizer.listen(source, timeout=10.0)
                sentence = recognizer.recognize_sphinx(audio)
                print(f"Recorded Sentence: {sentence}")

        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")

if __name__ == "__main__":
    while True:
        listen_and_record()
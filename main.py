from adhawk import EyeTracker
from liveimagery import LiveImagery
from threading import Thread
from narrator import text_to_speech 
from vision import *
from adhawk import *
import iris
import sounddevice as sd
import pygame

imagery = LiveImagery()
eyetracker = EyeTracker(imagery)

eyetracker_thread = Thread(target=eyetracker.start)
imagery_thread = Thread(target=imagery.display)

eyetracker_thread.start()
imagery_thread.start()

def play_wav_file(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

try:
	with sd.Stream(callback=iris.update_talking):
		while True:
			sd.sleep(1)

			words = iris.get_text().lower().split(' ')

			if words[0] == "find":
				play_wav_file("iris_sound.wav")
				text_to_speech("Finding " + ' '.join(words[1:]))

			elif "what am i looking at" in " ".join(words):
				play_wav_file("iris_sound.wav")
				if imagery.object_name == "unidentifiable object":
					text_to_speech("I don't know.")
				else:
					text_to_speech(f"You are looking at a {imagery.object_name}")

			elif "enable obstacle mode" in " ".join(words):
				play_wav_file("iris_sound.wav")
				text_to_speech("Turning obstacle detection mode on. Please tilt your head down to 45 degrees.")
				imagery.set_obstacle_mode(True)

			elif "disable obstacle mode" in " ".join(words):
				play_wav_file("iris_sound.wav")
				text_to_speech("Turning obstacle detection mode off")
				imagery.set_obstacle_mode(False)

			iris.set_text("")

except (KeyboardInterrupt, SystemExit):
	eyetracker.shutdown()
	imagery.shutdown()
	iris.close()

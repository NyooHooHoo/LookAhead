from adhawk import EyeTracker
from liveimagery import LiveImagery
from threading import Thread
from speech import listen_and_record
from narrator import text_to_speech 
from vision import *
from adhawk import *


imagery = LiveImagery()
eyetracker = EyeTracker(imagery)

eyetracker_thread = Thread(target=eyetracker.start)
imagery_thread = Thread(target=imagery.display)
eyetracker_thread.start()
imagery_thread.start()

try:
	while True:
		input_text = listen_and_record().lower()
		words = input_text.lower().split(' ')

		if words[0] == "find":
			text_to_speech("Finding " + ' '.join(words[1:]))
			

		elif input_text == "what am i looking at"
			# looking_at(localize_objects(),)

		elif input_text == "turn obstacle detection mode on"
			text_to_speech("Turning obstacle detection mode on")

		else:
				break
except (KeyboardInterrupt, SystemExit):
	eyetracker.shutdown()
	imagery.shutdown()

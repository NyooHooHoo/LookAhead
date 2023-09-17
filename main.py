from adhawk import EyeTracker
from liveimagery import LiveImagery
from threading import Thread
from speech import listen_and_record
from narrator import text_to_speech 


def main():
	imagery = LiveImagery()
	eyetracker = EyeTracker(imagery)

	eyetracker_thread = Thread(target=eyetracker.start)
	imagery_thread = Thread(target=imagery.display)
	eyetracker_thread.start()
	imagery_thread.start()
	
	try:
		while True:
			words = listen_and_record().split(' ')

			if "find" == words[0]:
				text_to_speech("Finding " + words[1:])
			else:
				break
	except (KeyboardInterrupt, SystemExit):
		eyetracker.shutdown()
		imagery.shutdown()


if __name__ == "__main__":
	main()

from adhawk import EyeTracker
from liveimagery import LiveImagery
from threading import Thread
from speech import listen_and_record


def main():
	imagery = LiveImagery()
	eyetracker = EyeTracker(imagery)

	eyetracker_thread = Thread(target=eyetracker.start)
	imagery_thread = Thread(target=imagery.display)
	eyetracker_thread.start()
	imagery_thread.start()
	
	try:
		while True:
			#words = listen_and_record()

			#if words[0] == "find":
			pass # sailesh do your thing

	except (KeyboardInterrupt, SystemExit):
		eyetracker.shutdown()
		imagery.shutdown()


if __name__ == "__main__":
	main()

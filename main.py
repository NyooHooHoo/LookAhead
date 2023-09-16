from adhawk import EyeTracker
from liveimagery import LiveImagery
from threading import Thread


def main():
	imagery = LiveImagery()
	eyetracker = EyeTracker()

	eyetracker_thread = Thread(target=eyetracker.start)
	imagery_thread = Thread(target=imagery.display)
	eyetracker_thread.start()
	imagery_thread.start()
	
	try:
		while True:
			pass
	except (KeyboardInterrupt, SystemExit):
		eyetracker.shutdown()
		imagery.shutdown()


if __name__ == "__main__":
	main()

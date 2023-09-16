from threading import Thread
import cv2


class LiveImagery:
	through_lens = None
	x, y = 0, 0

	def __init__(self):
		self.cap = cv2.VideoCapture(1)
		self.stop = False

	def display(self):
		while True:
			ret, through_lens = self.cap.read()
			width, height = through_lens.shape[:2]

			print(width, height)
	  
			cv2.imshow('webcam feed' , through_lens)

			if cv2.waitKey(1000) == ord('q'):
				break

	def update_information(args):
		print(args)

	def shutdown(self):
		self.stop = True


if __name__ == "__main__":
	imagery = LiveImagery()
	imagery.display()
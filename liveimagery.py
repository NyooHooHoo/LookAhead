from threading import Thread
import cv2


class LiveImagery:
	def __init__(self):
		self.cap = cv2.VideoCapture(1)
		self.stop = False

	def display(self):
		while True:
			key = cv2.waitKey(1) & 0xFF
			ret, frame = self.cap.read()
	  
			cv2.imshow('webcam feed' , frame)
			if self.stop:
				break

	def shutdown(self):
		self.stop = True


if __name__ == "__main__":
	imagery = LiveImagery()
	imagery.display()
from threading import Thread
import cv2


class LiveImagery:
	def __init__(self):
		self.cap = cv2.VideoCapture(1)

	def display(self):
		while True:
			key = cv2.waitKey(1) & 0xFF
			ret, frame = self.cap.read()
	  
			cv2.imshow('webcam feed' , frame)
			if key == 27:
				break


if __name__ == "__main__":
	imagery = LiveImagery()
	imagery.display()
from threading import Thread
import math
import cv2
import numpy as np
import vision


def draw_text(img, text,
          font=cv2.FONT_HERSHEY_PLAIN,
          pos=(0, 0),
          font_scale=1.5,
          font_thickness=1,
          color=(0,0,0),
          text_color_bg=(255,255,255)
        ):

    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, (x, y - 5), (x + text_w, y + text_h + 1), text_color_bg, -1)
    cv2.putText(img, text, (x, int(y + text_h + font_scale - 1)), font, font_scale, color, font_thickness)

    return text_size


def range_map(value, in_min, in_max, out_min, out_max):
	if math.isnan(value):
		return 0
	percentage = (value - in_min) / (in_max - in_min)
	return percentage * (out_max - out_min) + out_min;


def conv(x):
	return f'{x:.2f}'

N = 5
previous_N_sideeyes = [[-1, -1] for _ in range(0, N)]

def calculate_sideeyes(x, y):
	for i in range(0, N - 1):
		previous_N_sideeyes[i] = previous_N_sideeyes[i + 1]
	previous_N_sideeyes[N - 1] = (x, y)
	totalCounted = 0
	ret = [0, 0]

	for xi, yi in previous_N_sideeyes:
		if xi != -1 and yi != -1:
			totalCounted += 1
			ret[0] += xi
			ret[1] += yi

	for i in range(0, 2):
		ret[i] /= totalCounted
		ret[i] = int(ret[i])
	return tuple(ret)


class LiveImagery:
	def __init__(self):
		self.cap = cv2.VideoCapture(1)
		self.stop = False

		self.eye_center = {
			"left": {"x": 0, "y": 0, "z": 0},
			"right": {"x": 0, "y": 0, "z": 0}
		}
		self.gaze = {"x": 0, "y": 0, "z": 0, "vergence": 0}
		self.pupil_diameter = {"left": 0, "right": 0}
		self.IMU = {"x": 0, "y": 0, "z": 0, "w": 0}
		self.object_name = "unidentifiable object"

	def display_info(self, image):

		eye_center_text_left = f"""EYE CENTER: left (x: {conv(self.eye_center["left"]["x"])} y: {conv(self.eye_center["left"]["y"])} z: {conv(self.eye_center["left"]["z"])} )"""
		#draw_text(image, eye_center_text_left, pos=(5, 10))

		eye_center_text_right = f"""right (x: {conv(self.eye_center["right"]["x"])} y: {conv(self.eye_center["right"]["y"])} z: {conv(self.eye_center["right"]["z"])} )"""
		#draw_text(image, eye_center_text_right, pos=(5, 40))

		gaze_text = f"""GAZE: x: {conv(self.gaze["x"])} y: {conv(self.gaze["y"])} z: {conv(self.gaze["z"])} vergence: {conv(self.gaze["vergence"])}"""
		draw_text(image, gaze_text, pos=(5, 70))

		pupil_diamter_text = f"""PUPIL: left: {conv(self.pupil_diameter["left"])} right: {conv(self.pupil_diameter["left"])}"""
		#draw_text(image, pupil_diamter_text, pos=(5, 100))

		IMU_text = f"""IMU: x: {conv(self.IMU["x"])} y: {conv(self.IMU["y"])} z: {conv(self.IMU["z"])} w: {conv(self.IMU["w"])}"""
		#draw_text(image, IMU_text, pos=(5, 130))

		return image

	def get_crosshair_location(self):
		x = int(range_map(self.gaze["x"], -5, 5, 0, 639))
		if x < 0:
			x = 0
		elif x > 639:
			x = 639
		
		y = int(range_map(self.gaze["y"], -5, 5, 0, 479))
		if y < 0:
			y = 0
		elif y > 479:
			y = 479
		return x, y

	def draw_crosshair(self, image):
		x, y = self.get_crosshair_location()
		cv2.circle(image, calculate_sideeyes(x, y), 5, (0,0,255), -1)

		return image


	def display(self):
		while True:
			ret, frame = self.cap.read()
			cv2.imwrite("temp.jpg", frame)
			objects_ = vision.localize_objects(path="temp.jpg")

			areas, names = [], []
			for object_ in objects_:
				x1 = int(object_.bounding_poly.normalized_vertices[0].x * 640)
				y1 = int(object_.bounding_poly.normalized_vertices[0].y * 480)
				x2 = int(object_.bounding_poly.normalized_vertices[2].x * 640)
				y2 = int(object_.bounding_poly.normalized_vertices[2].y * 480)
				x, y = self.get_crosshair_location()
				if x1 <= x <= x2 and y1 <= y <= y2:
					areas.append((x2-x1)*(y2-y1))
					names.append(object_.name) 

				frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
			if names:
				self.object_name = names[areas.index(min(areas))]
				print(self.object_name)
			else:
				self.object_name = "unidentifiable object"

			frame = self.draw_crosshair(self.display_info(frame))
	
			cv2.imshow('LookAhead', frame)

			if cv2.waitKey(1) == ord('q'):
				break

	def update_information(self, args):
		self.eye_center = args["eye_center"]
		self.gaze = args["gaze"]
		self.pupil_diameter = args["pupil_diameter"]
		self.IMU = args["IMU"]

	def shutdown(self):
		self.stop = True


if __name__ == "__main__":
	imagery = LiveImagery()
	imagery.display()
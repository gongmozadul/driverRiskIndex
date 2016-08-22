##############
# FOR  HYUNDAI FIRST HACKATHON 2016, CONNECT THE UNCONNECTED!
# TEAM Gong-Mo-Ja-Dul
# 
# opencv view window module
##############

import cv2

class View:
	"""View windows using opencv2"""
	
	def __init__(self, title):
		self.title = title

	def setImage(self, image):
		self.image = image

	def resize(self, ratio):
		self.image = cv2.resize(self.image, (0,0), fx=ratio, fy=ratio)

	def show(self):
		cv2.imshow(self.title, self.image)

	def showDrive(self):
		pass

	def showMain(self, dir_arr, text_arr):
		# Draw Background
		height, width, channel = self.image.shape
		image = self.image.copy()
		
		cv2.rectangle(image, (0, 0), (width, height), (255, 255, 255), -1)
		cv2.addWeighted(image, 0.7, self.image, 0.3, 0, self.image)

		# Draw Picture
		car_img = cv2.imread('view/car.png', -1)
		img_height, img_width, chn = car_img.shape
		img_x = (width - img_width)/2
		img_y = 0
		for i in range(0, 3):
			self.image[img_y:img_y + img_height, img_x:img_x + img_width, i] = \
				car_img[:, :, i] * (car_img[:, :, 3]/255.0) + self.image[img_y:img_y + img_height, img_x:img_x + img_width, i] * (1.0 - car_img[:, :, 3]/255.0)

		# Draw Graph
		self.drawgraph(dir_arr, thickness=2)

		# Draw result
		for i in range(len(text_arr)):
			textsize = cv2.getTextSize(text_arr[i], cv2.FONT_HERSHEY_TRIPLEX, 0.7, 1)[0]
			text_x = (width - textsize[0]) / 2
			text_y = (height - textsize[1]) / 2 + 20
			cv2.putText(self.image, text_arr[i], (text_x, text_y + (textsize[1] * i * 2)), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 0))

		self.show()

	def drawgraph(self, dir_arr, x_gap=0.1, y_gap=0.05, thickness=1):
		height, width, channel = self.image.shape

		last_value = len(dir_arr) / 3
		if dir_arr[-1] < last_value:
			color = (0, 0, 255)
		elif dir_arr[-1] < last_value*2:
			color = (0, 255, 255)
		else:
			color = (0, 255, 0)

		# Graph Position
		x = int(round(width * x_gap))
		y = int(round(height - (height * y_gap)))

		# Graph Gap
		gap = (width - x * 2) / (len(dir_arr)-1)

		# Draw Standard Line
		cv2.line(self.image, (x, y - 50), (x + (gap * (len(dir_arr)-1)), y - 50), (128, 128, 128), thickness)

		# Draw graph
		for i in range(len(dir_arr) - 1):
			cv2.line(self.image, (x + (i * gap), y - dir_arr[i]), (x + ((i + 1) * gap), y - dir_arr[i + 1]), color, thickness)


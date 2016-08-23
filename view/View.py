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

	def setRedOverlay(self):
		height, width, channel = self.image.shape
		image = self.image.copy()
		
		cv2.rectangle(image, (0, 0), (width, height), (0, 0, 255), -1)
		cv2.addWeighted(image, 0.7, self.image, 0.3, 0, self.image)

	def showDrive(self, dri_arr, txt_arr):
		self.drawGraph(dri_arr, x_gap=0.01, y_gap=0.05, thickness=1, width_ratio=0.65)
		self.drawText(0.67, 0.05, txt_arr)
		cv2.putText(self.image, 'Driver Risk Index Calc., HYUNDAI Hackahton, Gong-mo-za-dul.', (0, 20),
                    cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 255, 255))
		self.show()

	def drawText(self, x_ratio, y_ratio, txt_arr):
		height, width, channel = self.image.shape
		x = int(round(width * x_ratio))
		y = height - int(round(height * y_ratio))
		# Draw Text
		for i in range(len(txt_arr)):
			cv2.putText(self.image, txt_arr[i], (x, y - (20 * i)), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255))

	def showMain(self, dri_arr, text_arr):
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
		self.drawGraph(dri_arr, thickness=2)

		# Draw result
		for i in range(len(text_arr)):
			textsize = cv2.getTextSize(text_arr[i], cv2.FONT_HERSHEY_TRIPLEX, 0.7, 1)[0]
			text_x = (width - textsize[0]) / 2
			text_y = (height - textsize[1]) / 2 + 20
			cv2.putText(self.image, text_arr[i], (text_x, text_y + (textsize[1] * i * 2)), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 0))

		self.show()

	def drawGraph(self, dri_arr, x_gap=0.1, y_gap=0.05, thickness=1, width_ratio=0):
		height, width, channel = self.image.shape

		if width_ratio != 0:
			width *= width_ratio
			width = int(round(width)) 

		if dri_arr[-1] < 33:
			color = (0, 255, 0)
		elif dri_arr[-1] < 66:
			color = (0, 255, 255)
		else:
			color = (0, 0, 255)

		# Graph Position
		x = int(round(width * x_gap))
		y = int(round(height - (height * y_gap)))

		# Graph Gap
		tmp = (len(dri_arr)-1)
		tmp = tmp if tmp != 0 else 1
		gap = (width - x * 2) / tmp

		# Draw Standard Line
		cv2.line(self.image, (x, y - 50), (x + (gap * (len(dri_arr)-1)), y - 50), (128, 128, 128), thickness)

		# Draw graph
		for i in range(len(dri_arr) - 1):
			cv2.line(self.image, (x + (i * gap), y - dri_arr[i]), (x + ((i + 1) * gap), y - dri_arr[i + 1]), color, thickness)


##############
# FOR  HYUNDAI FIRST HACKATHON 2016, CONNECT THE UNCONNECTED!
# TEAM Gong-Mo-Ja-Dul
# 
# view module
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

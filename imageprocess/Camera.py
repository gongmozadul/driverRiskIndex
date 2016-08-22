##############
# FOR  HYUNDAI FIRST HACKATHON 2016, CONNECT THE UNCONNECTED!
# TEAM Gong-Mo-Ja-Dul
# 
# camera module
##############

import cv2

class Camera:
	"""get camera image using opencv2"""
	cap = None
	
	def __init__(self, number, width, height):
		self.number = number
		self.width = width
		self.height = height

		self.cap = cv2.VideoCapture(self.number)
		self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.width)
		self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.height)

	def __del__(self):
		if self.cap != None:
			self.cap.release()
			try:
				self.cap.destroyAllWindows()
			except Exception, e:
				pass

	def getImage(self):
		return self.cap.read()

	def convertGray(self, image):
		return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
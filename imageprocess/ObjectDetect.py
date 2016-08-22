##############
# FOR  HYUNDAI FIRST HACKATHON 2016, CONNECT THE UNCONNECTED!
# TEAM Gong-Mo-Ja-Dul
# 
# object detect module
##############

import cv2

class ObjectDetect:
	"""object detect using opencv2"""
	option = None

	def __init__(self, xml_path):
		self.cascade = cv2.CascadeClassifier(xml_path)

	def setOption(self, dict_opt):
		self.option = dict_opt

	def detect(self, image):
		if self.option == None:
			return self.cascade.detectMultiScale(image)
		else:
			return self.cascade.detectMultiScale(image, **self.option)
##############
# FOR  HYUNDAI FIRST HACKATHON 2016, CONNECT THE UNCONNECTED!
# TEAM Gong-Mo-Ja-Dul
# 
# serial handle module
##############

import serial
import threading
import time

class serialLoop(threading.Thread):
	line = ""
	lock = threading.Lock()

	def __init__(self, port, baudrate):
		threading.Thread.__init__(self)
		self.__exit = False
		self.port = port
		self.baudrate = baudrate
		self.handle = serial.Serial(port, baudrate)
 
	def run(self):
		while True:
			### Process ###
			self.lock.acquire()
			self.line = self.handle.readline()
			# print self.line
			self.lock.release()
			time.sleep(0.001)

			### Exit ###
			if self.__exit:
				break

	def getLine(self):
		self.lock.acquire()
		line = self.line
		self.lock.release()		
		# line = "1.0-AAA-\n"
		# print self.line
		return line

	def Stop(self):
		self.__exit = True
		time.sleep(0.5)
		self.handle.close()

class Handle:
	"""handle sensor using pyserial"""

	def __init__(self, port, baudrate=9600):
		self.serial = serialLoop(port, baudrate)
		self.serial.start()

	def __del__(self):
		self.serial.Stop()

	def getPressure(self):
		txt = self.serial.getLine()
		# print txt
		value, category, tmp = txt.split('-')
		try:
			value = int(round(float(value)))
		except:
			value = 0

		return [category, value]

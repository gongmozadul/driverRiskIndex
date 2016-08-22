##############
# FOR  HYUNDAI FIRST HACKATHON 2016, CONNECT THE UNCONNECTED!
# TEAM Gong-Mo-Ja-Dul
# 
# main program
##############

# global modules
import cv2
import sys
from datetime import datetime
import pyaudio
import wave
import serial
import time
import threading
import SocketServer

# internal modules
import imageprocess
import view
# import handle as h
import data
data = data.Data

class beepLoop(threading.Thread):
	def __init__(self, path='beep.wav'):
		threading.Thread.__init__(self)
		self.__exit = False
		self.__beep = False
		
	def run(self):

		while True:
			time.sleep(0.1)

			if self.__beep:
				self.beep()

			### Exit ###
			if self.__exit:				
				break

	def Stop(self):
		self.__exit = True
		time.sleep(0.5)

	def beepStart(self):
		self.__beep = True

	def beepStop(self):
		self.__beep = False

	def beep(self):
		wf = wave.open('beep.wav', 'rb')
		pya = pyaudio.PyAudio()
		stream = pya.open(format=pya.get_format_from_width(wf.getsampwidth()),
						  channels=wf.getnchannels(),
						  rate=wf.getframerate(),
						  output=True)
		data = wf.readframes(1024)
		while data != '':
			stream.write(data)
			data = wf.readframes(1024)

		stream.close()
		pya.terminate()

class TcpLoop(threading.Thread):
	class MyTCPHandler(SocketServer.BaseRequestHandler):
		def handle(self):
			# self.request is the TCP socket connected to the client
			while True:
				self.data = self.request.recv(1).strip()
				print "{} wrote:".format(self.client_address[0])
				print self.data
				if self.data == '1':
					print '1'
					wf = wave.open('beep.wav', 'rb')
					pya = pyaudio.PyAudio()
					stream = pya.open(format=pya.get_format_from_width(wf.getsampwidth()),
									  channels=wf.getnchannels(),
									  rate=wf.getframerate(),
									  output=True)
					data = wf.readframes(1024)
					while data != '':
						stream.write(data)
						data = wf.readframes(1024)

					stream.close()
					pya.terminate()
				elif self.data == '0':
					print '0'
					break

	def __init__(self, beep):
		threading.Thread.__init__(self)
		self.__exit = False
		
	def run(self):
		server = SocketServer.TCPServer(("127.0.0.1", 39999), self.MyTCPHandler)
		self.server = server
		server.serve_forever()

	def Stop(self):
		self.server.shutdown()
		time.sleep(0.5)


def push_value(arr, limit, value):
	if len(arr) > limit:
		arr.pop(0)
	arr.append(value)

if __name__ == '__main__':

	maxW = 0
	maxH = 0
	camera_width = 320
	camera_height = 240
	oldX = camera_width / 2
	oldY = camera_height / 2
	oldCount = 0
	oldTime = time.time()
	state = 0
	MENU_STATE = 0
	DRIVE_STATE = 1
	txt_arr = []
	txt_limit = 20
	dri_arr = []
	dri_limit = 100

	camera = imageprocess.Camera(0, camera_width, camera_height)
	view = view.View("Drive Risk Index - GongMoJaDul")
	face = imageprocess.ObjectDetect("haarcascade_frontalface_default.xml")
	eye = imageprocess.ObjectDetect("haarcascade_eye.xml")
	beep = beepLoop()
	beep.start()
	tcp = TcpLoop(beep)
	tcp.start()
	# try:
	# 	handle = h.Handle("/dev/cu.usbmodem14221")
	# except serial.serialutil.SerialException:
	# 	print "SerialException"				

	face.setOption({
		'scaleFactor': 1.1,
		'minNeighbors': 5,
		'minSize': (30, 30),
		'flags': cv2.cv.CV_HAAR_SCALE_IMAGE
	})

	eye.setOption({
		'maxSize': (25, 25)
	})

	realtime = data('bigdata/realtime.csv')

	while True:
		inputed = cv2.waitKey(1) & 0xFF
		if inputed == ord('q'):
			break
		elif inputed == ord('s'):
			state = DRIVE_STATE
		elif inputed == ord('e'):
			state = MENU_STATE

		result = {
			'face': False,
			'eye': False,
			'view': 'NN'
		}

		ret, image = camera.getImage()
		image = cv2.flip(image, 1)

		if state == DRIVE_STATE:
			gray = camera.convertGray(image)

			faces = face.detect(gray)

			if len(faces) == 0:
				result['face'] = False
			else:
				result['face'] = True

			for (x, y, w, h) in faces:
				maxW = max(maxW, w)
				maxH = max(maxH, h)

				face_gray = gray[y:y+h, x:x+w]
				eyes = eye.detect(face_gray)
			
				if len(eyes) < 2:
					result['eye'] = False
				else:
					result['eye'] = True

				# sys.stdout.write(' '+str(maxH)+', '+str(maxW)+', '+str(w)+', '+str(h))

				overlay = image.copy()
				offset = 10
				for (ex,ey,ew,eh) in eyes:
					cv2.circle(overlay, (x+ex+offset,y+ey+offset),12,(255,0,0), -1)
					# cv2.rectangle(image,(x+ex,y+ey),(x+ex+ew,y+ey+eh),(255,0,0),2)
				opacity = 0.4
				cv2.addWeighted(overlay, opacity, image, 1 - opacity, 0, image)

				# cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

				# sys.stdout.write("          ")			
				# sys.stdout.write(str(oldX - x)+', '+str(oldY - y))
				# sys.stdout.write("          ")

				turnOffset = 10
				if oldX - x > turnOffset:
					result['view'] = 'R'
					cv2.arrowedLine(image, (x+w,(2*y+h)/2), (x,(2*y+h)/2), (0, 255, 0), thickness=2)
					# sys.stdout.write("R")
				elif oldX - x < -turnOffset:
					result['view'] = 'L'
					cv2.arrowedLine(image, (x,(2*y+h)/2), (x+w,(2*y+h)/2), (0, 255, 0), thickness=2)
					# sys.stdout.write("L")
				else:
					result['view'] = 'N'
					# sys.stdout.write("N")

				if oldY - y > turnOffset:
					result['view'] += 'U'
					cv2.arrowedLine(image, ((2*x+w)/2,y+h), ((2*x+w)/2,y), (0, 255, 0), thickness=2)
					# sys.stdout.write("U")
				elif oldY - y < -turnOffset:
					result['view'] += 'D'
					cv2.arrowedLine(image, ((2*x+w)/2,y), ((2*x+w)/2,y+h), (0, 255, 0), thickness=2)
					# sys.stdout.write("D")
				else:
					result['view'] += 'N'
					# sys.stdout.write("N")

				oldCount+=1
				if (oldCount > 20):
					oldCount = 0
					oldX = x
					oldY = y

				# sys.stdout.write("          ")

			sys.stdout.write("\r")
			sys.stdout.write(str(result))
			sys.stdout.flush()

			view.setImage(image)
			view.resize(2.5)

			# pressure = handle.getPressure()
			pressure = ['', 2000]

			newTime = time.time()
			row = None
			if newTime - oldTime > 1: # 1 second loop
				oldTime = newTime
				row = realtime.getRow()
				value, txt_arr2 = realtime.calcRealtimeIndex(row, pressure[1], result['eye'])
				value = 0
				if value == 100:
					beep.beepStart()
				else:
					beep.beepStop()
				# print value

				# push_value(dri_arr, dri_limit, pressure[1])
				push_value(dri_arr, dri_limit, value)

				for txt in txt_arr2:
					cur_time = datetime.now().strftime('%S.%f')[:-3]				
					push_value(txt_arr, txt_limit, cur_time + "  " + txt)
			elif row != None:
				value, txt_arr2 = realtime.calcRealtimeIndex(row, pressure[1], result['eye'])
				value = 0
				if value == 100:
					beep.beepStart()
				else:
					beep.beepStop()
				# print value

				# push_value(dri_arr, dri_limit, pressure[1])
				push_value(dri_arr, dri_limit, value)

				for txt in txt_arr2:
					cur_time = datetime.now().strftime('%S.%f')[:-3]				
					push_value(txt_arr, txt_limit, cur_time + "  " + txt)


			view.showDrive(dri_arr, txt_arr)

		elif state == MENU_STATE:
			summary = data('bigdata/summary.csv')

			dri_arr2 = []

			while True:
				row = summary.getRow()
				if row == False:
					break
				index = summary.calcSummaryIndex(row)
				# print index
				dri_arr2.append(index)

			txt_arr2 = summary.getSummaryText(dri_arr2)
			
			view.setImage(image)
			view.resize(2.5)
			view.showMain(dri_arr2, txt_arr2)
		
	# del(handle)
	beep.Stop()
	tcp.Stop()
















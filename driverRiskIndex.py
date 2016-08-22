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

# internal modules
import imageprocess
import view
import handle as h

def beep(filename='beep.wav'):
    wf = wave.open(filename, 'rb')
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
	handle = h.Handle("/dev/cu.usbmodem14221")

	face.setOption({
		'scaleFactor': 1.1,
		'minNeighbors': 5,
		'minSize': (30, 30),
		'flags': cv2.cv.CV_HAAR_SCALE_IMAGE
	})

	eye.setOption({
		'maxSize': (25, 25)
	})

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

				for (ex,ey,ew,eh) in eyes:
					cv2.rectangle(image,(x+ex,y+ey),(x+ex+ew,y+ey+eh),(255,0,0),2)

				cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

				# sys.stdout.write("          ")			
				# sys.stdout.write(str(oldX - x)+', '+str(oldY - y))
				# sys.stdout.write("          ")

				turnOffset = 10
				if oldX - x > turnOffset:
					result['view'] = 'R'
					# sys.stdout.write("R")
				elif oldX - x < -turnOffset:
					result['view'] = 'L'
					# sys.stdout.write("L")
				else:
					result['view'] = 'N'
					# sys.stdout.write("N")

				if oldY - y > turnOffset:
					result['view'] += 'U'
					# sys.stdout.write("U")
				elif oldY - y < -turnOffset:
					result['view'] += 'D'
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

			pressure = handle.getPressure()
			time = datetime.now().strftime('%S.%f')[:-3]

			push_value(dri_arr, dri_limit, pressure[1])
			push_value(txt_arr, txt_limit, time + "  " + pressure[0])

			view.showDrive(dri_arr, txt_arr)

		elif state == MENU_STATE:
			view.setImage(image)
			view.resize(2.5)
			view.showMain([10,50,100], ["ABCD"])
		
	del(handle)
















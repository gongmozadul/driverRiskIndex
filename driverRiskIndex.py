##############
# FOR  HYUNDAI FIRST HACKATHON 2016, CONNECT THE UNCONNECTED!
# TEAM Gong-Mo-Ja-Dul
# 
# main program
##############

# global modules
import cv2
import sys

# internal modules
import imageprocess

if __name__ == '__main__':

	maxW = 0
	maxH = 0
	camera_width = 320
	camera_height = 240
	oldX = camera_width / 2
	oldY = camera_height / 2
	oldCount = 0

	camera = imageprocess.Camera(0, camera_width, camera_height)
	view = imageprocess.View("Drive Risk Index - GongMoJaDul")
	face = imageprocess.ObjectDetect("haarcascade_frontalface_default.xml")
	eye = imageprocess.ObjectDetect("haarcascade_eye.xml")

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
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		result = {
			'face': False,
			'eye': False,
			'view': 'NN'
		}

		ret, image = camera.getImage()
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
		view.resize(2)
		view.show()
		# image = cv2.resize(image, (0,0), fx=2, fy=2)
		# cv2.imshow("Faces", image)

















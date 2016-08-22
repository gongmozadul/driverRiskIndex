# -*- coding: utf-8 -*-
##############
# FOR  HYUNDAI FIRST HACKATHON 2016, CONNECT THE UNCONNECTED!
# TEAM Gong-Mo-Ja-Dul
# 
# h drive data module
##############

import csv

class Data:
	"""h drive data module using csv"""
	eyeCount = 0

	def __init__(self, path):
		self.path = path
		self.f = open(self.path)
		self.csv = csv.reader(self.f)
		self.header = next(self.csv)

	def __del__(self):
		self.f.close()

	def getRow(self):
		try:
			return next(self.csv)
		except StopIteration:
			return False

	def calcSummaryIndex(self, row):
		return 30

	def getSummaryText(self, dri_arr):
		return ["ABCD"]

	def calcRealtimeIndex(self, row, pressure, eye):
		return self.calc_dri(int(row[7]), row[17], float(row[18]), pressure, float(row[13]), eye)

	def calc_dri(self, kph, road, grade, pressure, wheel_degree, eyeopen):

		print kph, road, grade, pressure, wheel_degree, eyeopen

		result = ["Road type: "+str(road), "Gradient: "+str(round(grade, 4)), "handle pressure: "+str(pressure), "wheel: "+str(wheel_degree), "eye open: "+str(eyeopen)]

		beep = 10000

		highway = 'E'
		nationalway = 'N'
		cityway = 'U'

		if road == highway:
			speed_min_limit = 50
			speed_max_limit = 120
		elif road == nationalway:
			speed_min_limit = 30
			speed_max_limit = 90
		elif road == cityway:
			speed_min_limit = 0
			speed_max_limit = 80
		else:
			speed_min_limit = 0
			speed_max_limit = 60

		# kph가 도로상태에 따라 최고나 초저 속도보다 높거나 낮으면 경고
		if kph >= speed_min_limit and kph <= speed_max_limit:
			# 속도가 적절한데 내리막일 경우 도로 최고 속도에 내리막 경사 * 2.5 를 더한값보다 속도가 크면 경고
			if speed_max_limit + grade * 0.5 > kph:
				speed = kph + grade * 0.5
				if speed <= 50:
					speed = 50
			else:
				speed = beep
		else:
			 speed = beep

		# 스티어링 각도가 500도에서 4.8 * kph 한거보다 작으면 위험하므로 경고
		if wheel_degree < (500 - 3.75 * kph):
			degree = (100 / (500 - 3.75 * kph))
		else:
			degree = beep

		# 압력이 속도 *25보다 작으면 압력이 모자란것이므로 경고
		if pressure < kph * 10:
			pressure = beep

		# 속도가 0 이상인데 눈을 1초이상 감고 있으면 경고
		if eyeopen is False:
			self.eyeCount += 1
		else:
			self.eyeCount = 0

		if self.eyeCount >= 2 and kph > 0:
			eye = beep
		else:
			eye = 0

		# dri를 계산
		dri = speed / 4 + degree * 5 + 25-(pressure / 100) + eye * 100

		print speed, degree, pressure, eye

		# dri가 100보다 클경우 100
		if dri > 100 or dri < 0:
			dri = 100

		return int(round(dri)), result





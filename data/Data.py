##############
# FOR  HYUNDAI FIRST HACKATHON 2016, CONNECT THE UNCONNECTED!
# TEAM Gong-Mo-Ja-Dul
# 
# h drive data module
##############

import csv

class Data:
	"""h drive data module using csv"""

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

	def calcRealtimeIndex(self, row):
		return 70, ["BCDE"]



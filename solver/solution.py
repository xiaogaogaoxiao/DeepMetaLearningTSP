import sys
import numpy

from .utilities import calculateCost

class Solution(object):
	def __init__(self, tsp, optimalTour):
		self.tsp = tsp
		self.optimalTour = optimalTour
		self.features = {}
		self.solutions = {}
		
	def addFeature(self, name, value):
		self.features[name] = value

	def addProblemSolution(self, name):
		problemSolution = ProblemSolution()
		self.solutions[name] = problemSolution
		return problemSolution

class ProblemSolution(object):
	def __init__(self):
		self.best = None
		self.bestCost = sys.maxsize
		self.worst = None
		self.worstCost = 0
		self.averageCost = 0
		self.solutions = []

	def addTour(self, tour, cost):
		self.solutions.append({"tour": tour, "cost": cost})

		if cost < self.bestCost:
			self.best = tour
			self.bestCost = cost

		if cost > self.worstCost:
			self.worst = tour
			self.worstCost = cost

		averageCost = len(self.solutions)

	def updateAverage(self):
		length = len(self.solutions)

		if length == 0:
			self.averageCost = 0
			return

		sumValue = 0
		for solution in self.solutions:
			sumValue += solution["cost"]

		self.averageCost = sumValue/self.averageCost

class OptimalTour(object):
	def __init__(self, tour, tsp):
		self.tour = numpy.array(tour)
		self.cost = calculateCost(self.tour, tsp)
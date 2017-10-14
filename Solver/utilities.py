import numpy
import random

def generateInitialSolution(tsp):
	size = tsp.getSize()

	solution = numpy.arange(size)

	for index in range(size):
		randomIndex = random.randrange(index, size)
		temp = solution[index]
		solution[index] = solution[randomIndex]
		solution[randomIndex] = temp

	return solution

def calculateCost(solution, tsp):
	cost = 0

	if solution.shape[0] < 2:
		return cost

	previous = None
	current = solution[0]

	for i in range(1, solution.shape[0]):
		temp = solution[i]

		cost += tsp.getCost(current, temp)

		previous = current
		current = temp

	# Add cost of returning from last to first
	cost += tsp.getCost(current, solution[0])

	return cost
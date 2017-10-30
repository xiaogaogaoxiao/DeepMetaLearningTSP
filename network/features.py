# Utilities

from collections import defaultdict, deque
from solver.utilities import calculateCost
import sys
import numpy

def vertexCost(tsp, index):
	sumValue = 0

	for i in range(0, tsp.getSize()):
		sumValue += tsp.getCost(i, index)
		sumValue += tsp.getCost(index, i)

	# 2 times as many costs as points
	return sumValue/(tsp.getSize()*2)

def buildVertexCosts(tsp):
	costs = numpy.array(tsp.getSize())

	for city in range(0, tsp.getSize()):
		costs[city] = vertexCost(tsp, city)

	return costs

# From Gist https://gist.github.com/mdsrosa/c71339cb23bc51e711d8
def dijkstra(tsp, initial):
	visited = {initial: 0}
	path = {}

	nodes = set(range(tsp.getSize()))

	while nodes:
		min_node = None
		for node in nodes:
			if node in visited:
				if min_node is None:
					min_node = node
				elif visited[node] < visited[min_node]:
					min_node = node
		if min_node is None:
			break

		nodes.remove(min_node)
		current_weight = visited[min_node]

		for second_node in range(tsp.getSize()):
			try:
				weight = current_weight + tsp.getCost(min_node, second_node)
			except:
				continue
			if second_node not in visited or weight < visited[second_node]:
				visited[second_node] = weight
				path[second_node] = min_node

	return visited, path


def dijkstraShortestPath(tsp, origin, destination):
	visited, paths = dijkstra(tsp, origin)
	full_path = deque()
	_destination = paths[destination]

	while _destination != origin:
		full_path.appendleft(_destination)
		_destination = paths[_destination]

	full_path.appendleft(origin)
	full_path.append(destination)

	return visited[destination], list(full_path)

# Solution selection

def greedySolutions(tsp, n):
	solutions = []

	for i in range(n):
		initial = numpy.random.randint(tsp.getSize())
		solution = [initial]

		while len(solution) < tsp.getSize():
			last = solution[-1]

			minCity = 0
			minCost = sys.maxsize
			for city in range(tsp.getSize()):
				if city == last:
					continue

				cost = tsp.getCost(last, city)

				if cost < minCost:
					minCity = city
					minCost = cost

			solution.append(city)

		solutions.append(numpy.array(solution))

	return solutions

def neighborSolutions(tsp, solution, n):
	solutions = []

	for i in range(n):
		newSolution = numpy.copy(solution)
		selected = numpy.random.randint(tsp.getSize())

		if selected == tsp.getSize() - 1:
			# Swap with first element
			newSolution[selected] = solution[0]
			newSolution[0] = solution[selected]
		else:
			newSolution[selected] = solution[selected + 1]
			newSolution[selected + 1] = solution[selected]

		solutions.append(solution)

	return solutions

def bestNeighborSolution(tsp, solution, n):
	solutions = neighborSolutions(tsp, solution, n)

	bestSolution = None
	minCost = sys.maxsize

	for i in range(n):
		cost = calculateCost(solutions[i], tsp)

		if cost < minCost:
			minCost = cost
			bestSolution = solutions[i]

	return bestSolution

from .asymTSP import AsymmetricTSP
from .symTSP import SymmetricTSP
from .solution import OptimalTour
import math

def loadTSPLib(path):
	try:
		file = open(path, "r")

		name = ""
		instanceType = None
		dimension = 0

		pointsLine = -1
		pointFormat = None
		points = []

		for line in file:
			if pointsLine == -1:
				split = line.split(":")
				attribute = split[0].strip().lower()
				value = None

				if len(split) > 1:
					value = split[1].strip().lower()

				if attribute == "name":
					name = value
				elif attribute == "type":
					instanceType = value
				elif attribute == "dimension":
					dimension = int(value)
				elif attribute == "node_coord_section":
					pointFormat = "node_coord_section"
					pointsLine = 0
				elif attribute == "edge_weight_format":
					pointFormat = value
				elif attribute == "edge_weight_section":
					pointsLine = 0
			else:
				line = line.strip()
				
				if line == "EOF":
					break

				line = " ".join(line.split())
				split = line.split(" ")
				print(split)

				if pointFormat == "node_coord_section":
					if len(split) != 3:
						print("Malformed input")
						return None

					points.append((float(split[1]), float(split[2])))
				elif pointFormat == "full_matrix":
					if len(split) != dimension:
						print("Malformed input")
						return None

					for (i, value) in enumerate(split):
						points.append((i, pointsLine, float(value)))

				pointsLine += 1

		if instanceType == "tsp":
			if dimension < 1 or dimension != len(points):
				print("Invalid dimensions")
				return None
			tsp = SymmetricTSP(dimension)

			for i in range(dimension):
				p1 = points[i]

				for j in range(dimension):
					if i < j:
						p2 = points[j]
						cost = euclidianDistance2D(p1[0], p1[1], p2[0], p2[1])
						tsp.setCost(i, j, cost)
						tsp.setCost(j, i, cost)

				# Add diagonal
				tsp.setCost(i, i, 0)
				tsp.setAdjacent(i, i, False)

			return tsp
		elif instanceType == "atsp":
			tsp = AsymmetricTSP(dimension)

			for point in points:
				i = point[0]
				j = point[1]
				cost = point[2]

				tsp.setCost(i, j, cost)

			# Add diagonal
			for i in range(dimension):
				tsp.setAdjacent(i, i, False)

			return tsp

		else:
			print("Invalid instance type")
			return None


	except FileNotFoundError:
		print("File not found")
		return None

def loadTSPLibTour(path, tsp):
	try:
		file = open(path, "r")

		name = ""
		instanceType = None
		dimension = 0

		enteredPoints = False
		points = []

		for line in file:
			if not enteredPoints:
				split = line.split(":")
				attribute = split[0].strip().lower()
				value = None

				if len(split) > 1:
					value = split[1].strip().lower()

				if attribute == "name":
					name = value
				elif attribute == "type":
					instanceType = value
				elif attribute == "dimension":
					dimension = int(value)
				elif attribute == "tour_section":
					enteredPoints = True
			else:
				line = line.strip()
				
				if line == "EOF" or line == "-1":
					break

				index = -1
				try:
					index = int(line)
				except:
					print("Malformed input")
					return None

				# Subtract 1, since indicies are 1 indexed in TSPLib
				points.append(index - 1)

		if dimension < 1 or dimension != len(points):
			print("Invalid dimensions")
			return None

		if instanceType == "tour":
			tour = OptimalTour(points, tsp)

			return tour
		else:
			print("Invalid instance type %s" % (instanceType))
			return None

	except FileNotFoundError:
		print("File not found")
		return None

def euclidianDistance2D(x1, y1, x2, y2):
	deltaX = x1 - x2
	deltaY = y1 - y2

	return math.sqrt(deltaX*deltaX + deltaY*deltaY)

def euclidianDistance3D(x1, y1, z1, x2, y2, z2):
	deltaX = x1 - x2
	deltaY = y1 - y2
	deltaZ = z1 - z2

	return math.sqrt(deltaX*deltaX + deltaY*deltaY + deltaZ*deltaZ)

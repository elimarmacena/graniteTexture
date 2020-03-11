import numpy as np

def startHistogram(size_histogram:int):
	histogram_dict = {}
	for i in range(size_histogram):
		histogram_dict[i] = 0
	return histogram_dict

def sumMatrixData(matrix:np.array):
	sum_data = 0
	for line in matrix:
		for column in line:
			sum_data += column
	return sum_data
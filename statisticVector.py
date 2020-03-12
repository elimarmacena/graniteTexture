import numpy as np
import mct as mct8
import commons
from math import pow

def statisticVector(matrix_input:np.array, SUBDIV=2):
	segment_information = []
	for current_level in range(SUBDIV):
		# @matrix_inpu subdivision
		segmented_matrix = _sectionMatrix(matrix_input,(current_level + 1))
		for segment in segmented_matrix:
			segment_information.extend(_getSegmentInformation(segment))
	return segment_information

	

def _sectionMatrix(matrix_full:np.array, level_subregion:int):
	secmentation = int(level_subregion * 2)
	line_section = len(matrix_full) // secmentation
	column_section = len(matrix_full[0]) // secmentation
	line_interaction = 0
	column_interaction = 0
	list_matrix_section = []

	line_end = 0
	while ( line_interaction < secmentation):
		column_end = 0
		column_interaction = 0
		while(column_interaction < secmentation):
			#getting window from the current section
			slice_matrix = matrix_full[line_end:(line_end + line_section),column_end:(column_end+column_section)]
			column_end += column_section
			column_interaction += 1
			list_matrix_section.append(slice_matrix)
		line_end += line_section
		line_interaction += 1
	return np.array(list_matrix_section)

def _getSegmentInformation(matrix:np.array):
	num_row = len(matrix)
	num_col = len(matrix[0])
	#is used a 3 x 3 window to compute the constrat value
	if(num_row < 3 or num_col < 3):
		#raise Exception('Matrix size is not valid')
		return None
	row_agent = 0
	constrast_vet = []
	mct8_vet = []
	while(row_agent <= (num_row - 3)):
		column_agent = 0
		while(column_agent <= (num_col - 3)):
			current_window = matrix[row_agent:(row_agent+3),column_agent:(column_agent+3)]
			# contrast computed based in OJALA formule
			# VARp = (1/P) Sum(Ip - μ)^2
			window_size = len(current_window[0]) * len(current_window)
			# @mu_value = μ letter
			mu_value = _getMuValue(current_window)
			sum_result = _getSumWindowMu(current_window, mu_value)
			constrast_value = (1/window_size)*sum_result
			constrast_vet.append(constrast_value)
			sum_window_values = commons.sumMatrixData(current_window)
			mct8_window = mct8._findMctWindow(current_window, (sum_window_values // 9))
			mct8_vet.append(mct8_window)
			column_agent += 1
		row_agent += 1
	vet_result = [np.mean(constrast_vet),np.mean(mct8_vet),np.var(mct8_vet)]
	return (np.asarray(vet_result))

def _getMuValue(matrix_section):
	mu_amount = 0
	pixel_amout = 0
	for line in matrix_section:
		for column  in line:
			mu_amount += column
			pixel_amout += 1
	mu_value = 1/pixel_amout
	mu_value = mu_value * mu_amount
	return mu_value

def _getSumWindowMu(matrix_window:np.array,mu_value):
	sum_values = 0
	for line in matrix_window:
		for cell in line:
			cell_information = cell - mu_value
			sum_values = sum_values + pow(cell_information,2)
	return int(sum_values)

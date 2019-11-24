import numpy as np
from math import pow
def contrastVAR(matrix:np.array):
	sectioned_matrix = _sectionMatrix(matrix, 4)
	sub_sectioned_matrix = []

	contrast_result = []
	#create the sub secment at the matrix
	#compute of the first part of contrast
	for piece in sectioned_matrix:
		contrast_result.append(contrastCompute(piece))
		sub_sectioned_matrix.extend(_sectionMatrix(piece,4))
	
	#compute of the contrast of the subsection
	contrast_result_subsection = []
	for sub_piece in sub_sectioned_matrix:
		contrast_result_subsection.append(contrastCompute(sub_piece))
	return contrast_result,contrast_result_subsection

def contrastCompute(matrix:np.array):
	num_row = len(matrix)
	num_col = len(matrix[0])
	#is used a 3 x 3 window to compute the constrat value
	if(num_row < 3 or num_col < 3):
		#raise Exception('Matrix size is not valid')
		return None
	row_agent = 0
	constrast_vet = []
	while(row_agent <= (num_row - 3)):
		column_agent = 0
		while(column_agent <= (num_col - 3)):
			current_window = matrix[row_agent:(row_agent+3),column_agent:(column_agent+3)]
			#contrast computed based in OJALA formule
			#VARp = (1/P) Sum(Ip - u)^2
			window_size = len(current_window[0]) * len(current_window)
			mu_value = _getMuValue(current_window)
			sum_result = _getSumWindowMu(current_window, mu_value)
			constrast_value = (1/window_size)*sum_result
			constrast_vet.append(constrast_value)
			column_agent += 1
		row_agent += 1
	return (np.asarray(constrast_vet))

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

# only working for pair numbers
def _sectionMatrix(matrix_full:np.array, number_section:int):
	secmentation = int(number_section / 2)
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

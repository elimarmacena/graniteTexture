import numpy as np
from descriptors import mct as mct8
from utils import commons
from math import pow

def statisticVector(matrix_input:np.array, SUBDIV=2):
	segment_information = []
	for current_level in range(SUBDIV):
		# @matrix_inpu subdivision
		segmented_matrix = _sectionMatrix(matrix_input,(current_level + 1))
		for segment in segmented_matrix:
			segment_information.extend(getSectionStatistics(segment))
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

def getSectionStatistics(matrix:np.array):
	num_row = len(matrix)
	num_col = len(matrix[0])
	#is used a 3 x 3 window to compute the constrat value
	if(num_row < 3 or num_col < 3):
		#raise Exception('Matrix size is not valid')
		return None
	row_agent = 0
	constrast_vet = []
	mct8_vet = []
	while(row_agent < num_row):
		column_agent = 0
		while(column_agent < num_col):
			# top_left, top_middle, top_right, 
			macro_data = [get_neighbor(row_agent-1,column_agent-1,matrix),get_neighbor(row_agent-1, column_agent,matrix),get_neighbor(row_agent-1,column_agent+1,matrix),
			# middle_left, middle_middle, middle_right,
			get_neighbor(row_agent,column_agent-1,matrix),get_neighbor(row_agent,column_agent,matrix),get_neighbor(row_agent, column_agent+1,matrix),
			# bot_left, bot_middle, bot_right, 
			get_neighbor(row_agent+1,column_agent-1,matrix),get_neighbor(row_agent+1, column_agent,matrix),get_neighbor(row_agent+1,column_agent+1,matrix)]
			current_window = matrix[row_agent:(row_agent+3),column_agent:(column_agent+3)]
			# @mu_value = μ letter
			mu_value = getMuValue(macro_data)
			sum_result = getInformationSum(macro_data, mu_value)
			# contrast computed based in OJALA formule
			# VARp = (1/P) Sum(Ip - μ)^2
			constrast_value = (1/9)*sum_result
			constrast_vet.append(constrast_value)
			sum_window_values = commons.sumMatrixData(current_window)
			mct8_window = mct8.getMctValue(current_window, (sum_window_values // 9))
			mct8_vet.append(mct8_window)
			column_agent += 1
		row_agent += 1
	vet_result = [np.mean(constrast_vet),np.mean(mct8_vet),np.var(mct8_vet)]
	return (np.asarray(vet_result))

def getMuValue(macro_list):
	mu_amount = 0
	pixel_amout = 9
	for value  in macro_list:
		mu_amount += value
	mu_value = 1/pixel_amout
	mu_value = mu_value * mu_amount
	return mu_value

def getInformationSum(macro_list,mu_value):
	sum_values = 0
	for value in macro_list:
		cell_information = value - mu_value
		sum_values = sum_values + np.power(cell_information,2)
	return int(sum_values)

def get_neighbor(row_index:int,column_index:int,matrix:np.array):
	try:
		if(row_index >= 0 and column_index >= 0):
			return matrix[row_index][column_index]
		else:
			return 0
	except IndexError:
		return 0
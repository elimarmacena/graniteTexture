import numpy as np
from mct import getMctValue
from multiprocessing import Process, Array, Value
def statisticVector(matrix_input:np.array, SUBDIV = 2, NUM_PROC = 4):
	segment_infomration = list()
	for current_level in range(SUBDIV):
		segmented_matrix = getSections(matrix_input,(current_level + 1))
		for segment in segmented_matrix:
			segment_infomration.extend(getSectionStatistics(segment,NUM_PROC))
	return segment_infomration

def getSections(matrix_full:np.array, level_subregion:int):
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

def getSectionStatistics(matrix:np.array,num_proc):
	num_row = len(matrix)
	num_col = len(matrix[0])
	contrast_array = Array('f',[0]* ((num_row-2) * (num_col-2)),lock=False)
	mct8_array = Array('f',[0]* ((num_row-2) * (num_col-2)),lock=False)
	current_line = Value('I', 0)
	process_list = list()
	for i in range(num_proc):
		p = Process(target=work_space,args=(matrix,contrast_array,mct8_array,current_line))
		process_list.append(p)
		p.start()
	for worker in process_list:
		worker.join()
	vet_result = [np.mean(contrast_array[:]), np.mean(mct8_array[:]), np.var(mct8_array[:])]
	return np.asarray(vet_result)

def work_space(matrix:np.array,contrast_array, mct8_array,current_line):
	local_line = 0
	max_row = len(matrix)
	while (current_line.value <= (max_row - 3)):
		with current_line.get_lock():
			local_line = current_line.value
			current_line.value +=1
		local_col = 0
		max_col = len(matrix[local_line])
		while(local_col <= (max_col -3)):
			current_window = matrix[local_line:(local_line + 3), local_col:(local_col + 3)]
			mu_value = getMuValue(current_window)
			information_sum = getInformationSum(current_window,mu_value)
			contrast_value = (1/9) * information_sum
			mct_value = getMctValue(current_window, int(np.mean(current_window)))
			contrast_array[((max_row -2) * local_line)+local_col] = contrast_value
			mct8_array[((max_row -2) * local_line)+local_col] = mct_value
			local_col +=1

#Rewrite using numpy functions
def getMuValue(macro_matrix):
	mu_amount = 0
	pixel_amout = 0
	for line in macro_matrix:
		for column  in line:
			mu_amount += column
			pixel_amout += 1
	mu_value = 1/pixel_amout
	mu_value = mu_value * mu_amount
	return mu_value

def getInformationSum(macro_matrix,mu_value):
	sum_values = 0
	for line in macro_matrix:
		for cell in line:
			cell_information = cell - mu_value
			sum_values = sum_values + pow(cell_information,2)
	return int(sum_values)
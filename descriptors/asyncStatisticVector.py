import numpy as np
from descriptors.asyncMct import getMctValue
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
	contrast_array = Array('f',[0]* ((num_row) * (num_col)),lock=False)
	mct8_array = Array('f',[0]* ((num_row) * (num_col)),lock=False)
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
	with current_line.get_lock():
		local_line = current_line.value
		current_line.value +=1
	while (local_line < max_row):
		local_col = 0
		max_col = len(matrix[local_line])
		while(local_col < max_col):
			# top_left, top_middle, top_right, 
			macro_data = [get_neighbor(local_line-1,local_col-1,matrix),get_neighbor(local_line-1, local_col,matrix),get_neighbor(local_line-1,local_col+1,matrix),
			# middle_left, middle_middle, middle_right,
			get_neighbor(local_line,local_col-1,matrix),get_neighbor(local_line,local_col,matrix),get_neighbor(local_line, local_col+1,matrix),
			# bot_left, bot_middle, bot_right, 
			get_neighbor(local_line+1,local_col-1,matrix),get_neighbor(local_line+1, local_col,matrix),get_neighbor(local_line+1,local_col+1,matrix)]
			#current_window = matrix[local_line:(local_line + 3), local_col:(local_col + 3)]
			mu_value = getMuValue(macro_data)
			information_sum = getInformationSum(macro_data,mu_value)
			contrast_value = (1/9) * information_sum
			mct_value = getMctValue(macro_data, int(np.mean(macro_data)))
			contrast_array[((max_row -2) * local_line)+local_col] = contrast_value
			mct8_array[((max_row -2) * local_line)+local_col] = mct_value
			local_col +=1
		# End col while
		with current_line.get_lock():
			local_line = current_line.value
			current_line.value +=1
	# End line while

#Rewrite using numpy functions
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
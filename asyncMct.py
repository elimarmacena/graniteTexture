import numpy
from multiprocessing import Process, Array, Value
import commons

def mct(matrix:numpy.array, num_process = 1):
	num_row = len(matrix)
	num_col = len(matrix[0])
	process_list = list()
	current_line = Value('I',0)
	histogram = Array('I',[0]*256)
	mct_array = Array('I',[0] * ((num_row) * (num_col)),lock=False)
	# Process creation
	for i in range(num_process):
		p = Process(target=work_center, args=(histogram, current_line, matrix, mct_array))
		process_list.append(p)
		p.start()
	# Waiting for the processes
	for worker in process_list:
		worker.join()
	# Convert the 1d array into a 2d
	mct_matrix = numpy.array(mct_array[:]).reshape(num_row, num_col)
	return (mct_matrix, numpy.array(histogram[:]))

def work_center(histogram, current_line, matrix, mct_array):
	# Variable used to keep the current line and release the lock between the processes
	local_line = 0
	max_row = len(matrix)
	while(current_line.value < max_row):
		with current_line.get_lock():
			local_line = current_line.value
			current_line.value += 1
		local_col = 0
		while(local_col < len(matrix[0])):
			# top_left, top_middle, top_right, 
			macro_data = [get_neighbor(local_line-1,local_col-1,matrix),get_neighbor(local_line-1, local_col,matrix),get_neighbor(local_line-1,local_col+1,matrix),
			# middle_left, middle_middle, middle_right,
			get_neighbor(local_line,local_col-1,matrix),get_neighbor(local_line,local_col,matrix),get_neighbor(local_line, local_col+1,matrix),
			# bot_left, bot_middle, bot_right, 
			get_neighbor(local_line+1,local_col-1,matrix),get_neighbor(local_line+1, local_col,matrix),get_neighbor(local_line+1,local_col+1,matrix)]
			avg_window = int(numpy.mean(macro_data[:]))
			mct_value = getMctValue(macro_data,avg_window)
			# Critial zone, just one process per time can execute the increment
			with histogram.get_lock():
				histogram[mct_value] += 1
			mct_array[((max_row - 2) * local_line) + local_col] = mct_value
			local_col += 1

def getMctValue(neighborhood_list,avg_value):
	bit_string = ''
	neighborhood = [neighborhood_list[0],neighborhood_list[1],neighborhood_list[2],neighborhood_list[5],neighborhood_list[8],neighborhood_list[7],neighborhood_list[6],neighborhood_list[3]]
	for neighbor_value in neighborhood:
		bit_string = bit_string + ('1' if (neighbor_value >= avg_value) else '0')

	return int(bit_string,2)

def get_neighbor(row_index:int,column_index:int,matrix:numpy.array):
	try:
		if(row_index >= 0 and column_index >= 0):
			return matrix[row_index][column_index]
		else:
			return 0
	except IndexError:
		return 0
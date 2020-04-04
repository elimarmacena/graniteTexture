import numpy
from multiprocessing import Process, Array, Value
import commons

def mct(matrix:numpy.array, num_process = 4):
	num_row = len(matrix)
	num_col = len(matrix[0])
	if(num_row < 3 or num_col < 3):
		raise Exception('Matrix size is not valid')
	process_list = list()
	current_line = Value('I',0)
	histogram = Array('I',[0]*256)
	mct_array = Array('I',[0] * ((num_row - 2) * (num_col - 2)),lock=False)
	# Process creation
	for i in range(num_process):
		p = Process(target=work_center, args=(histogram, current_line, matrix, mct_array))
		process_list.append(p)
		p.start()
	# Waiting for the processes
	for worker in process_list:
		worker.join()
	# Convert the 1d array into a 2d
	mct_matrix = numpy.array(mct_array[:]).reshape(num_row-2, num_col-2)
	return (mct_matrix, numpy.array(histogram[:]))

def work_center(histogram, current_line, matrix, mct_array):
	# Variable used to keep the current line and release the lock between the processes
	local_line = 0
	max_row = len(matrix)
	while(current_line.value <= max_row - 3):
		with current_line.get_lock():
			local_line = current_line.value
			current_line.value += 1
		local_col = 0
		while(local_col <= len(matrix[0]) - 3):
			current_window = matrix[local_line:(local_line+3),local_col:(local_col+3)]
			avg_window = int(numpy.mean(current_window[:]))
			mct_value = getMctValue(current_window,avg_window)
			# Critial zone, just one process per time can execute the increment
			with histogram.get_lock():
				histogram[mct_value] += 1
			mct_array[((max_row - 2) * local_line) + local_col] = mct_value
			local_col += 1

def getMctValue(window,avg_value):
	bit_string = ''
	
	#First Line
	top_left		=	window[0][0]
	top_middle		=	window[0][1]
	top_right		=	window[0][2]

	#Second Line
	middle_left		=	window[1][0]
	middle_right	=	window[1][2]

	#Final Line
	bottom_left		=	window[2][0]
	bottom_middle	=	window[2][1]
	bottom_right	=	window[2][2]

	neighborhood = [top_left,top_middle,top_right,middle_right,bottom_right,bottom_middle,bottom_left,middle_left]
	for neighbor_value in neighborhood:
		bit_string = bit_string + ('1' if (neighbor_value >= avg_value) else '0')

	return int(bit_string,2)
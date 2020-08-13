import numpy as np
from multiprocessing import Process, Array, Value
from utils import commons
def ctdn(matrix:np.array, num_proc = 6):
	num_row = len(matrix)
	num_col = len(matrix[0])
	if(num_row < 9 or num_col < 9):
		raise Exception('Matrix size is not valid')
	process_list = list()
	current_line = Value('I', 0)
	histogram = Array('I',[0]*256)
	for i in range(num_proc):
		p = Process(target=work_center,args=(histogram,current_line,matrix))
		process_list.append(p)
		p.start()
	for worker in process_list:
		worker.join()
	return np.array(histogram[:])

def work_center(histogram, current_line, matrix):
	local_line = 0
	k_value = 4
	max_row = len(matrix)
	with current_line.get_lock():
		local_line = current_line.value
		current_line.value += 1
	while(local_line < max_row):
		local_col = 0
		while(local_col <len(matrix[0])):
			# top_left, top_middle, top_right, 
			macro_data = [get_neighbor(local_line-1,local_col-1,matrix),get_neighbor(local_line-1, local_col,matrix),get_neighbor(local_line-1,local_col+1,matrix),
			# middle_left, middle_middle, middle_right,
			get_neighbor(local_line,local_col-1,matrix),get_neighbor(local_line,local_col,matrix),get_neighbor(local_line, local_col+1,matrix),
			# bot_left, bot_middle, bot_right, 
			get_neighbor(local_line+1,local_col-1,matrix),get_neighbor(local_line+1, local_col,matrix),get_neighbor(local_line+1,local_col+1,matrix)]

			# top_left, top_middle, top_right, 
			farther_neighborhood = [get_neighbor(local_line-k_value,local_col-k_value,matrix),get_neighbor(local_line-k_value,local_col,matrix),get_neighbor(local_line-k_value,local_col+k_value,matrix),
			# middle_left, middle_right,
			get_neighbor(local_line,local_col-k_value,matrix),get_neighbor(local_line,local_col+k_value,matrix),
			# bot_left, bot_middle, bot_right, 
			get_neighbor(local_line+k_value,local_col-k_value,matrix),get_neighbor(local_line+k_value,local_col,matrix),get_neighbor(local_line+k_value,local_col+k_value,matrix)]
			
			ctdn_value = getCtdnValue(macro_data,farther_neighborhood)
			with histogram.get_lock():
				histogram[ctdn_value] += 1
			local_col += 1
		# End col while
		with current_line.get_lock():
			local_line = current_line.value
			current_line.value += 1
	# End line while

def getCtdnValue(center_window_data,farther_window_data):
	center_avg = int(np.mean(center_window_data))
	# top_left,top_middle,top_right,middle_right,bottom_right,bottom_middle,bottom_left,middle_left
	ctdn_order = [farther_window_data[0],farther_window_data[1],farther_window_data[2],farther_window_data[4],farther_window_data[7],farther_window_data[6],farther_window_data[5],farther_window_data[3]]
	neighbors_sum = np.sum(ctdn_order)
	bit_string = ''
	for pixel_value in ctdn_order:
		is_great = pixel_value >= ((neighbors_sum + center_avg) // 9)
		bit_string = bit_string + ('1' if is_great else '0')
	return int(bit_string,2)

def get_neighbor(row_index:int,column_index:int,matrix:np.array):
	try:
		if(row_index >= 0 and column_index >= 0):
			return matrix[row_index][column_index]
		else:
			return 0
	except IndexError:
		return 0
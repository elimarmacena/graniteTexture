import numpy as np
from multiprocessing import Process, Array, Value
import commons
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
	max_row = len(matrix)
	while(current_line.value <= (max_row - 9)):
		with current_line.get_lock():
			local_line = current_line.value
			current_line.value += 1
		local_col = 0
		while(local_col <= len(matrix[0])- 9):
			macro_img = matrix[local_line:(local_line+9), local_col:(local_col + 9)]
			ctdn_value = getCtdnValue(macro_img)
			with histogram.get_lock():
				histogram[ctdn_value] += 1
			local_col += 1

def getCtdnValue(macro_matrix, k_value = 4):
	central_begin = k_value - 1
	central_end = k_value + 2
	central_matrix = macro_matrix[central_begin:central_end,central_begin:central_end]
	center_avg = int(np.mean(central_matrix))
	top_left        =   macro_matrix[0][0]
	top_middle      =   macro_matrix[0][k_value]
	top_right       =   macro_matrix[0][k_value * 2]
	middle_left     =   macro_matrix[k_value][0]
	middle_right    =   macro_matrix[k_value][k_value * 2]
	bottom_left     =   macro_matrix[k_value * 2][0]
	bottom_middle   =   macro_matrix[k_value * 2][k_value]
	bottom_right    =   macro_matrix[k_value * 2][k_value * 2]

	ctdn_order = [top_left,top_middle,top_right,middle_right,bottom_right,bottom_middle,bottom_left,middle_left]
	neighbors_sum = np.sum(ctdn_order)
	bit_string = ''
	for pixel_value in ctdn_order:
		is_great = pixel_value >= ((neighbors_sum+ center_avg) // 9)
		bit_string = bit_string + ('1' if is_great else '0')
	return int(bit_string,2)
from utils import commons as Commons
import numpy as np

def ctdn(matrix:np.array):
	k_value = 4
	num_row = len(matrix)
	num_col = len(matrix[0])
	if (num_row < 9 or num_col < 9):
		raise Exception('Matrix size is not valid')
	ctdn_histogram = Commons.startHistogram(256)
	row_agent = 0
	while(row_agent < num_row):
		column_agent = 0
		while(column_agent < num_col):
			# top_left, top_middle, top_right, 
			macro_data = [get_neighbor(row_agent-1,column_agent-1,matrix),get_neighbor(row_agent-1, column_agent,matrix),get_neighbor(row_agent-1,column_agent+1,matrix),
			# middle_left, middle_middle, middle_right,
			get_neighbor(row_agent,column_agent-1,matrix),get_neighbor(row_agent,column_agent,matrix),get_neighbor(row_agent, column_agent+1,matrix),
			# bot_left, bot_middle, bot_right, 
			get_neighbor(row_agent+1,column_agent-1,matrix),get_neighbor(row_agent+1, column_agent,matrix),get_neighbor(row_agent+1,column_agent+1,matrix)]

			# top_left, top_middle, top_right, 
			farther_neighborhood = [get_neighbor(row_agent-k_value,column_agent-k_value,matrix),get_neighbor(row_agent-k_value,column_agent,matrix),get_neighbor(row_agent-k_value,column_agent+k_value,matrix),
			# middle_left, middle_right,
			get_neighbor(row_agent,column_agent-k_value,matrix),get_neighbor(row_agent,column_agent+k_value,matrix),
			# bot_left, bot_middle, bot_right, 
			get_neighbor(row_agent+k_value,column_agent-k_value,matrix),get_neighbor(row_agent+k_value,column_agent,matrix),get_neighbor(row_agent+k_value,column_agent+k_value,matrix)]

			ctdn_value = getCtdnValue(macro_data,farther_neighborhood)
			ctdn_histogram[ctdn_value] += 1
			column_agent +=1
		# End column while
		row_agent += 1
	#End row while
	return np.array(ctdn_histogram)

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
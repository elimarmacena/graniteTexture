# as default the function work the algorith using the 8bits approach
# having 2^8 values possible
import numpy as np
import commons as Commons

def mct(matrix:np.array, approach=8):
	num_row = len(matrix)
	num_col = len(matrix[0])
	row_agent = 0
	mct_matrix = []
	mct_histogram = Commons.startHistogram(256)
	while(row_agent < num_row):
		column_agent = 0
		mct_line = []
		while(column_agent <= (num_col - 3)):
			# top_left, top_middle, top_right, 
			macro_data = [get_neighbor(row_agent-1,column_agent-1,matrix),get_neighbor(row_agent-1, column_agent,matrix),get_neighbor(row_agent-1,column_agent+1,matrix),
			# middle_left, middle_middle, middle_right,
			get_neighbor(row_agent,column_agent-1,matrix),get_neighbor(row_agent,column_agent,matrix),get_neighbor(row_agent, column_agent+1,matrix),
			# bot_left, bot_middle, bot_right, 
			get_neighbor(row_agent+1,column_agent-1,matrix),get_neighbor(row_agent+1, column_agent,matrix),get_neighbor(row_agent+1,column_agent+1,matrix)]
			window_sum = np.sum(macro_data)
			avg_window = window_sum // 9
			mct_value = getMctValue(macro_data,avg_window)
			mct_line.append(mct_value)
			mct_histogram[mct_value] += 1
			column_agent += 1
		# End column while
		mct_matrix.append(mct_line)
		row_agent += 1
	# End row while
	return (np.asarray(mct_matrix),mct_histogram)


def getMctValue(neighborhood_list,avg_value):
	bit_string = ''

	# top_left, top_middle, top_right, 
	neighborhood = [neighborhood_list[0],neighborhood_list[1],neighborhood_list[2],
	# middle_right,bot_right, bot_middle,
	neighborhood_list[5],neighborhood_list[8],neighborhood_list[7],
	# bot_left, middle_left,
	neighborhood_list[6],neighborhood_list[3]]
	
	for neighbor_value in neighborhood:
		bit_string = bit_string + ('1' if (neighbor_value >= avg_value) else '0')

	return int(bit_string,2)

def get_neighbor(row_index:int,column_index:int,matrix:np.array):
	try:
		if(row_index >= 0 and column_index >= 0):
			return matrix[row_index][column_index]
		else:
			return 0
	except IndexError:
		return 0
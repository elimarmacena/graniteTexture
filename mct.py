# as default the function work the algorith using the 8bits approach
# having 2^8 values possible
import numpy as np
import commons as Commons

def mct(matrix, approach=8):
	num_row = len(matrix)
	num_col = len(matrix[0])
	if(num_row < 3 or num_col < 3):
		raise Exception('Matrix size is not valid')
	row_agent = 0
	mct_matrix = []
	mct_histogram = Commons.startHistogram(256)
	while(row_agent <= (num_row - 3)):
		column_agent = 0
		mct_line = []
		while(column_agent <= (num_col - 3)):
			current_window = [matrix[row_agent][column_agent:column_agent+3], matrix[row_agent+1]
							  [column_agent:column_agent+3], matrix[row_agent+2][column_agent:column_agent+3]]
			window_sum = _makeWindowSum(current_window)
			avg_window = window_sum // 9
			mct_value = _findMctWindow(current_window,avg_window)
			mct_line.append(mct_value)
			mct_histogram[mct_value] += 1
			column_agent += 1
			
		mct_matrix.append(mct_line)
		row_agent += 1
	return (np.asarray(mct_matrix),mct_histogram)


def _makeWindowSum(window):
	sum_window = 0
	for l in range(len(window)):
		for c in range(len(window[l])):
			sum_windowum = sum_window + window[l][c]
	return sum_window

def _findMctWindow(window,avg_value):
	string_bit = ''
	is_great = False
	
	#Top line
	cells_first_line = len(window[0])
	for tl in range(cells_first_line):
		is_great = window[0][tl] >= avg_value
		string_bit = string_bit + ('1' if is_great else '0')
	
	#Left coloumn
	total_columns = len(window)
	#ignore the fist information, already check in the previous loop
	for lc in range(1,total_columns):
		is_great = window[lc][len(window)-1] >= avg_value
		string_bit = string_bit + ('1' if is_great else '0')
	
	#Bottom line
	final_line_index = len(window)-1
	total_cells_final_line = len(window[final_line_index]) 
	#ignore last cell, already check in the previous loop
	for bl in range(total_cells_final_line - 2,-1,-1):
		is_great = window[len(window)-1][bl] >= avg_value
		string_bit = string_bit + ('1' if is_great else '0')
	
	#Right column
	#ignore values already checked in the previous loops (first value of the first line and first value of the last line)
	for rc in range(len(window)-2,0,-1):
		is_great = window[rc][0] >= avg_value
		string_bit = string_bit +('1' if is_great else '0')
	return int(string_bit,2)


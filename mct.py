# as default the function work the algorith using the 8bits approach
# having 2^8 values possible


def mct(matrix, approach=8):
	num_row = len(matrix)
	num_column = len(matrix[0])
	if(num_row < 3 and num_column < 3):
		raise Exception('Matrix size is not valid')
	row_agent = 0
	mct_matrix = []
	while(row_agent <= (num_row - 2)):
		column_agent = 0
		mct_line = []
		while(column_agent <= (num_column - 2)):
			current_window = [matrix[row_agent][num_column:num_column+2], matrix[row_agent+1]
							  [num_column:num_column+2], matrix[row_agent+2][num_column:num_column+2]]
			window_sum = _makeWindowSum(current_window)
			avg_window = window_sum // 9
			window_mct = _findMctWindow(current_window,avg_window)

	return 0


def _makeWindowSum(window):
	sum = 0
	for l in range(len(window)):
		for c in range(len(window[l])):
			sum = sum + window[l][c]
	return sum

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
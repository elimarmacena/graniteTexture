# as default the function work the algorith using the 8bits approach
# having 2^8 values possible
import numpy as np
import commons as Commons

def mct(matrix:np.array, approach=8):
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
			#getting a window from the image
			current_window = matrix[row_agent:(row_agent+3),column_agent:(column_agent+3)]
			window_sum = Commons.sumMatrixData(current_window)
			avg_window = window_sum // 9
			mct_value = _findMctWindow(current_window,avg_window)
			mct_line.append(mct_value)
			mct_histogram[mct_value] += 1
			column_agent += 1
			
		mct_matrix.append(mct_line)
		row_agent += 1
	return (np.asarray(mct_matrix),mct_histogram)


def _findMctWindow(window,avg_value):
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


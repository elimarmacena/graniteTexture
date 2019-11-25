import commons as Commons
import numpy as np

def ctdn(matrix:np.array):
    num_row = len(matrix)
    num_col = len(matrix[0])
    if(num_row < 9 or num_col < 9):
        raise Exception('Matrix size is not valid')
    row_agent = 0
    ctdn_matrix = []
    ctdn_histogram = Commons.startHistogram(256)
    while(row_agent < (len(num_row) - 9)):
        column_agent = 0
        ctdn_line = []
        while(column_agent < (len(num_col) -9)):
            current_window = matrix[row_agent:(row_agent+9),column_agent:(column_agent+9)]
            avg_center_window = _centerAvg(current_window)
            ctdn_value = _findCtdnWindow(current_window,avg_center_window)
            ctdn_line.append(ctdn_value)
            ctdn_histogram[ctdn_value] += 1
            column_agent += 1
        ctdn_matrix.append(ctdn_line)
        row_agent += 1
    return (np.asarray(ctdn_matrix),ctdn_histogram)

def _centerAvg(nine_window):
    center_window = [nine_window[3][3:6],nine_window[4][3:6],nine_window[5][3:6]]
    sum_center = 0
    for line in center_window:
        for value in line:
            sum_center += value
    return sum_center // 9

def _findCtdnWindow(nine_window,avg):
    bit_string = ''
    is_great = False
    size_first_line = len(nine_window[0])
    for fl in range(0,size_first_line,4):
        is_great = nine_window[0][fl] >= avg
        bit_string = bit_string + ('1' if is_great else '0')
    size_column = len(nine_window[len(nine_window)-1])
    for fc in range(0,size_column,4):
        is_great = nine_window[fc][len(nine_window)-1]
        bit_string = bit_string + ('1' if is_great else '0')
    size_last_line = len(nine_window[len(nine_window)-1])
    for ls in range(size_last_line-5,-1,-4):
        is_great = nine_window[len(nine_window)-1][ls]
        bit_string = bit_string + ('1' if is_great else '0')
    is_great = nine_window[0][size_column-5]
    bit_string = bit_string + ('1' if is_great else '0')
    return int(bit_string,2)
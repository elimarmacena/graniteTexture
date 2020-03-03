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
    while(row_agent < (num_row - 9) ):
        column_agent = 0
        ctdn_line = []
        while(column_agent < (num_col -9)):
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

# In our study K means 4
def _findCtdnWindow(nine_window,avg):
    bit_string = ''
    is_great = False
    size_first_line = len(nine_window[0])
    for fl in range(0,size_first_line,4):
        is_great = nine_window[0][fl] >= avg
        bit_string = bit_string + ('1' if is_great else '0')
    #TODO: change the values 4 and 8 to a viable representing the value of K and K*2 
    is_great = nine_window[0+4][0+8] >= avg 
    bit_string = bit_string + ('1' if is_great else '0')
    size_last_line = len(nine_window[len(nine_window)-1])
    for ls in range(size_last_line-5,-1,-4):
        is_great = nine_window[len(nine_window)-1][ls] >= avg
        bit_string = bit_string + ('1' if is_great else '0')
    #TODO: change the value 4 to a viable representing the value of K
    is_great = nine_window[0 + 4][0] #this will be change to a variable seting the value of K 
    bit_string = bit_string + ('1' if is_great else '0')
    return int(bit_string,2)
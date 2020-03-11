import commons as Commons
import numpy as np

def ctdn(matrix:np.array):
    num_row = len(matrix)
    num_col = len(matrix[0])
    if (num_row < 9 or num_col < 9):
        raise Exception('Matrix size is not valid')
    ctdn_histogram = Commons.startHistogram(256)
    row_agent = 0
    while(row_agent < (num_row - 9)):
        column_agent = 0
        while(column_agent < (num_col - 9)):
            # the gap used are 9 because of the size of center matrix 3x3 plus the K value, in our work 4
            macro_img = matrix[row_agent:(row_agent + 9),column_agent:(column_agent + 9)]
            ctdn_value = _findCtdnWindow(macro_img)
            ctdn_histogram[ctdn_value] += 1
            column_agent +=1
        row_agent += 1
    return ctdn_histogram

def _findCtdnWindow(macro_matrix:np.array, k_value = 4):
    # index center matrix start
    center_begin = k_value - 1 
    center_end = k_value + 2
    
    center_matrix = macro_matrix[center_begin: center_end, center_begin: center_end]
    center_avg = Commons.sumMatrixData(center_matrix)

    top_left        =   macro_matrix[0][0]
    top_middle      =   macro_matrix[0][k_value]
    top_right       =   macro_matrix[0][k_value * 2]
    middle_left     =   macro_matrix[k_value][0]
    middle_right    =   macro_matrix[k_value][k_value * 2]
    bottom_left     =   macro_matrix[k_value * 2][0]
    bottom_middle   =   macro_matrix[k_value * 2][k_value]
    bottom_right    =   macro_matrix[k_value * 2][k_value * 2]

    ctdn_order = [top_left,top_middle,top_right,middle_right,bottom_right,bottom_middle,bottom_left,middle_left]
    bit_string = ''
    for pixel_value in ctdn_order:
        is_great = pixel_value >= ((pixel_value + center_avg) // 9)
        bit_string = bit_string + ('1' if is_great else '0')
    return int(bit_string,2)
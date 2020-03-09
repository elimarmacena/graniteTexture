import numpy as np
import commons as Commons
def lbp(matrix:np.array):
    num_row = len(matrix)
    num_col = len(matrix[0])
    if(num_row < 3 or num_col < 3 ):
        raise Exception('Matrix size is not valid')
    row_agent = 0
    lbp_histogram = Commons.startHistogram(256)
    while(row_agent <= (num_row - 3)):
        column_agent = 0
        while(column_agent <= (num_col - 3)):
            #sub image with a size equals 3x3
            macro_img = matrix[row_agent:(row_agent+3),column_agent:(column_agent+3)]
            lbp_value = _findLbpMacro(macro_img)
            lbp_histogram[lbp_value] += 1
            column_agent += 1
        row_agent +=1
    return lbp_histogram
            
def _findLbpMacro(matrix:np.array):
    middle          = matrix[1][1]
    #matrix first line
    top_left        = matrix[0][0]
    top_middle      = matrix[0][1]
    top_right       = matrix[0][2]
    
    #matrix second line
    middle_left     = matrix[1][0]
    middle_right    = matrix[1][2]
    
    #matrix final line
    bottom_left     = matrix[2][0]
    bottom_middle   = matrix[2][1]
    bottom_right     = matrix[2][2]

    lbp_order = [top_left,middle_left,bottom_left,bottom_middle,bottom_right,middle_right,top_right,top_middle]
    value = _macroValue(lbp_order, middle)
    return value

def _macroValue(neighborhood:list, center_value:int):
    bit_string = ''
    for neighbor_value in neighborhood:
        bit_string = bit_string + ('1' if (neighbor_value >= center_value) else '0')
    return int(bit_string,2)
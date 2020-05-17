import numpy as np
import commons as Commons
def lbp(file_locate:str):
    matrix = Commons.imgToMatrix(file_locate)
    num_row = len(matrix)
    num_col = len(matrix[0])
    row_agent = 0
    lbp_histogram = Commons.startHistogram(256)
    while(row_agent < num_row):
        column_agent = 0
        while(column_agent <num_col):
            # top_left, top_middle, top_right, 
            macro_data = [get_neighbor(row_agent-1,column_agent-1,matrix),get_neighbor(row_agent-1, column_agent,matrix),get_neighbor(row_agent-1,column_agent+1,matrix),
            # middle_left, middle_right,
            get_neighbor(row_agent,column_agent-1,matrix),get_neighbor(row_agent, column_agent+1,matrix),
            # bot_left, bot_middle, bot_right, 
            get_neighbor(row_agent+1,column_agent-1,matrix),get_neighbor(row_agent+1, column_agent,matrix),get_neighbor(row_agent+1,column_agent+1,matrix)]
            middle_pixel = get_neighbor(row_agent,column_agent,matrix)
            
            lbp_value = bit_value(macro_data,middle_pixel)
            lbp_histogram[lbp_value] += 1
            column_agent += 1
        row_agent +=1
    return lbp_histogram
            
def bit_value(neighborhood:list, center_value:int):
    counter_clockwise = [neighborhood[0],neighborhood[3],neighborhood[5],neighborhood[6],neighborhood[7],neighborhood[4],neighborhood[2],neighborhood[1]]
    bit_string = ''
    for neighbor_value in counter_clockwise:
        bit_string = bit_string + ('1' if (neighbor_value >= center_value) else '0')
    return int(bit_string,2)

def get_neighbor(row_index:int,column_index:int,matrix:np.array):
    try:
        if(row_index >= 0 and column_index >= 0):
            return matrix[row_index][column_index]
        else:
            return 0
    except IndexError:
        return 0
    
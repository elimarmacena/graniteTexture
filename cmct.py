import asyncMct as mct
from commons import imgToMatrix
def cmct(image:str):
    #gray image matrix
    image_matrix = imgToMatrix(image)
    #first find mct8 of the original image
    mct_original,histogram_original = mct.mct(image_matrix)
    #recursive data
    mct_recursive, histogram_recursive = mct.mct(mct_original)
    #histogram concatenation
    cmct_histogram = histogram_concate(histogram_original,histogram_recursive)
    return cmct_histogram


def histogram_concate(first_histogram:dict, second_histogram:dict):
    final_histogram =  [None] * 512
    for i in range(256):
        final_histogram[i]          =   first_histogram[i]
        final_histogram[i + 256]    =   second_histogram[i]
    return final_histogram

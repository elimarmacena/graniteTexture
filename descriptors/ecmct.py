from utils.commons import imgToMatrix
from descriptors import cmct
from descriptors import ctdn
from descriptors import asyncStatisticVector
from descriptors import asyncCtdn

def ecmct(file_locate:str,cmct_precal = list()):
    # Is possible to receive the cmct result as parameter, this way we can avoid unnecessary calc
    cmct_histogram = cmct_precal if(cmct_precal != []) else cmct.cmct(file_locate)
    
    #loading the file as a matrix
    image_matrix = imgToMatrix(file_locate)

    #getting the ctdn information
    ctdn_histogram = asyncCtdn.ctdn(image_matrix)

    #getting the contrast information
    statistic_info =  asyncStatisticVector.statisticVector(image_matrix)

    #information concatenation
    ecmct_histogram = []
    ecmct_histogram.extend(cmct_histogram)
    ecmct_histogram.extend(ctdn_histogram)
    ecmct_histogram.extend(statistic_info)
    
    return ecmct_histogram
from commons import imgToMatrix
import cmct
import ctdn
import asyncStatisticVector
import asyncCtdn

def ecmct(file_locate:str):
    #getting the cmct from the file
    cmct_histogram = cmct.cmct(file_locate)
    
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
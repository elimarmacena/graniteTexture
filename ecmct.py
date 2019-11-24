import imgMatrix as ImgUtil
import cmct
import ctdn
import contrastLevel as Contrast

def ecmct(file_locate:str):
    #getting the cmct from the file
    cmct_histogram = cmct.cmct(file_locate)
    
    #loading the file as a matrix
    image_matrix = ImgUtil.imgToMatrix(file_locate)

    #getting the ctdn information
    ctdn_matrix,ctdn_histogram = ctdn.ctdn(image_matrix)

    #getting the contrast information
    section_contrast,subsection_contrast =  Contrast.contrastVAR(image_matrix)

    #information concatenation
    ecmct_histogram = []
    ecmct_histogram.extend(cmct_histogram)
    ecmct_histogram.extend(ctdn_histogram)
    ecmct_histogram.extend(section_contrast)
    ecmct_histogram.extend(subsection_contrast)
    
    return ecmct_histogram
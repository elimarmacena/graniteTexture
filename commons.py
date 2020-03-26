import numpy as np
import glob
from PIL import Image
import sys
from os.path import dirname, abspath
diretorio = dirname(dirname(abspath(__file__)))
sys.path.append(diretorio)

def imgToMatrix(fileLocation: str):
    # open the passed image as a grayscale image
    image = Image.open(fileLocation).convert('L')
    img_ar = np.asarray(image)
    return(img_ar)

def startHistogram(size_histogram:int):
	histogram_dict = [0]*size_histogram
	return histogram_dict

def sumMatrixData(matrix:np.array):
	sum_data = 0
	for line in matrix:
		for column in line:
			sum_data += column
	return sum_data

def summaryzeImgPaths():
	path_images = getAllImages()
	image_sumary = {}
	for image in path_images:
		tokenized_path = image.split('\\')
		granite_type = tokenized_path[-1].split('_')[0]
		paths_type = image_sumary[granite_type] if (granite_type in image_sumary.keys()) else []
		paths_type.append(image)
		image_sumary[granite_type] = paths_type
	return image_sumary

def getAllImages():
    # images are currently divided into folders inside the master folder
    master_folder = '.\\GraniteImgs\\*\\*'
    image_path = glob.glob(master_folder)
    return image_path

def writeFile(file_path:str):
	file_data = open(file_path, 'w')
	return file_data

def addFileLine(line_content:str, file_data):
	file_data.write(line_content)

def closeFile(file_data):
	file_data.close()
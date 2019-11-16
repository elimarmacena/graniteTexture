import numpy as np
from PIL import Image
import sys
from os.path import dirname, abspath
diretorio = dirname(dirname(abspath(__file__)))
sys.path.append(diretorio)


def imgToMatrix(fileLocation: str):
    # open the passed image as a gray scale image
    image = Image.open(fileLocation).convert('L')
    img_ar = np.asarray(image)
    return(img_ar)

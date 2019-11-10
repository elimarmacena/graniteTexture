from PIL import Image
import numpy as np
def imgToMatrix(fileLocation:str):
    image = Image.open(fileLocation)
    img_ar = np.asarray(image)
    return(img_ar)
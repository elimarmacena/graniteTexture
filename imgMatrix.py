from PIL import Image
import numpy as np
def imgToMatrix(fileLocation:str):
    #open the passed image as a gray scale image
    image = Image.open(fileLocation).convert('LA')
    img_ar = np.asarray(image)
    return(img_ar)
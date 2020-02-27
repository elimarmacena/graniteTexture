import cmct as cmct
import time
import numpy as np
import contrastLevel as cl
import imgMatrix as im
import statisticVector
def main():
  # start_time = time.time()
  img_locate = 'GraniteImgs/00/VerdeMing_A_00_03.bmp'
  # histogram = cmct.cmct(img_locate)
  # print('--- %s SECONDS' %(time.time() - start_time))
  # print(histogram)
  a = im.imgToMatrix(img_locate)
  #test = np.array(a)
  
  c = statisticVector.statisticVector(a)
  # for i in b:
  #   print(len(b))
 
  print (c)
  print(len(c))
if __name__== "__main__":
  main()

import cmct as cmct
import time

def main():
  start_time = time.time()
  img_locate = 'GraniteImgs/00/VerdeMing_A_00_03.bmp'
  histogram = cmct.cmct(img_locate)
  print('--- %s SECONDS' %(time.time() - start_time))
  print(histogram)
  
  
if __name__== "__main__":
  main()

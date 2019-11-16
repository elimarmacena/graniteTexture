import mct as mct
import imgMatrix as im
import time
def main():
  start_time = time.time()
  print(start_time)
  img_locate = 'GraniteImgs/00/AcquaMarina_A_00_01.bmp'
  test_open = im.imgToMatrix(img_locate)
  mct.mct(matrix=test_open)
  print('--- %s SECONDS' %(time.time() - start_time))
  #matrix = [[180,180,180],[90,150,200],[91,151,201]]
  #print(mct.mct(matrix=matrix))
  # mct._findMctWindow(matrix,avg)
  
if __name__== "__main__":
  main()

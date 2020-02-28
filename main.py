import cmct as cmct
import time
import imgMatrix as im
import statisticVector
import imageSearch
def main():

	img_locate = 'GraniteImgs/00/VerdeMing_A_00_03.bmp'
	a = im.imgToMatrix(img_locate)
	
	start_time = time.time()
	c = statisticVector.statisticVector(a)
	print('--- %s SECONDS' %(time.time() - start_time))
	
	print (c)
	print(len(c))
if __name__== "__main__":
  main()

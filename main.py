
import time
import imgMatrix as im
#import statisticVector
import ecmct
import imageSearch
def main():

	img_locate = 'GraniteImgs/00/VerdeMing_A_00_03.bmp'
	a = im.imgToMatrix(img_locate)
	
	start_time = time.time()
	c = ecmct.ecmct(img_locate)
	print('--- %s SECONDS' %(time.time() - start_time))
	
	print (c)
if __name__== "__main__":
  main()

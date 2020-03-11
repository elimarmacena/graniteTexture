
import time
import ctdn
import imageSearch
import imgMatrix as imgUtil
def main():
	img_path = imageSearch.getAllImages()
	
	lbp_histogram = ctdn.ctdn(imgUtil.imgToMatrix(img_path[0]))
	print(lbp_histogram)
if __name__== "__main__":
  main()

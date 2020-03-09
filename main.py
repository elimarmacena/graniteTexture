
import time
import lbp
import imageSearch
import imgMatrix as imgUtil
def main():
	img_path = imageSearch.getAllImages()
	
	lbp_histogram = lbp.lbp(imgUtil.imgToMatrix(img_path[0]))
	print(lbp_histogram)
if __name__== "__main__":
  main()

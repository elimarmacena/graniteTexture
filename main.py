
import time
import ctdn
import imageSearch
import imgMatrix as imgUtil
# TODO save each algorith information in a CSV file
def main():
	img_path = imageSearch.getAllImages()
	test_img = img_path[0]
	granite_dic = {}
	for img in img_path:
		token_path = img.split('\\')
		granite_type = token_path.pop().split('_').pop(0)
		past_value = granite_dic[granite_type] if (granite_type in granite_dic.keys()) else 0
		granite_dic[granite_type] = past_value + 1
	print(granite_dic)
	print(len(granite_dic.keys()))
if __name__== "__main__":
  main()

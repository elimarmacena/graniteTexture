import time
from utils import commons
from Descriptors import ecmct as ecmct
from Descriptors import lbp as lbp
from Descriptors import cmct as cmct

def main():
	start_time = time.time()
	summary_path = commons.summaryzeTexturePaths()
	lbp_file = commons.writeFile('lbp__results.csv')
	cmct_file = commons.writeFile('cmct_results.csv')
	ecmct_file = commons.writeFile('ecmct_results.csv')
	for class_texture  in summary_path.keys():
		for img_path in summary_path[class_texture]:
			print(f'IMAGE: {img_path} START')
			# LBP SECTION
			lbp_histogram = lbp.lbp(img_path)
			commons.addFileLine(''+img_path + ',' + (','.join(str(index_value) for index_value in lbp_histogram )) + '\n', lbp_file)
			# CMCT SECTION
			cmct_histogram = cmct.cmct(img_path)
			commons.addFileLine(''+img_path + ',' + (','.join(str(index_value) for index_value in cmct_histogram )) + '\n', cmct_file)
			# ECMCT SECTION
			ecmct_histogram = ecmct.ecmct(img_path,cmct_precal=cmct_histogram)
			commons.addFileLine(''+img_path + ',' + (','.join(str(index_value) for index_value in ecmct_histogram )) + '\n', ecmct_file)
	
	commons.closeFile(lbp_file)
	commons.closeFile(cmct_file)
	commons.closeFile(ecmct_file)
	print('All images are now processed')
	print('--- %s SECONDS' %(time.time() - start_time))
if __name__== "__main__":
  main()

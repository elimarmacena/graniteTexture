import time
import commons
import ecmct
import lbp
import cmct

def main():
	summary_path = commons.summaryzeTexturePaths()
	lbp_file = commons.writeFile('lbp_texture_results.csv')
	cmct_file = commons.writeFile('cmct_texture_results.csv')
	ecmct_file = commons.writeFile('ecmct_texture_result.csv')
	for class_texture  in summary_path.keys():
		for img_path in summary_path[class_texture]:
			print(f'IMAGE: {img_path} START\n')
			# LBP SECTION
			lbp_histogram = lbp.lbp(img_path)
			commons.addFileLine(''+img_path + ',' + (','.join(str(index_value) for index_value in lbp_histogram )) + '\n', lbp_file)
			# CMCT SECTION
			cmct_histogram = cmct.cmct(img_path)
			commons.addFileLine(''+img_path + ',' + (','.join(str(index_value) for index_value in cmct_histogram )) + '\n', cmct_file)
			# ECMCT SECTION
			ecmct_histogram = ecmct.ecmct(img_path)
			commons.addFileLine(''+img_path + ',' + (','.join(str(index_value) for index_value in ecmct_histogram )) + '\n', ecmct_file)
	
	commons.closeFile(lbp_file)
	commons.closeFile(cmct_file)
	commons.closeFile(ecmct_file)
	print('All images are now processed')
if __name__== "__main__":
  main()

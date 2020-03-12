
import time
import commons
import ecmct
import lbp
import cmct
# TODO save each algorith information in a CSV file
def main():
	summary_path = commons.summaryzeImgPaths()
	lbp_file = commons.writeFile('lbp_results.csv')
	cmct_file = commons.writeFile('cmct_results.csv')
	ecmct_file = commons.writeFile('ecmct_result.csv')
	
	for granite_type  in summary_path.keys():
		for img_path in summary_path[granite_type]:
			# LBP SECTION
			lbp_histogram = lbp.lbp(img_path)
			commons.addFileLine(''+img_path + ',' + (','.join(str(index_value) for index_value in lbp_histogram )) + '\n', lbp_file)
			#CMCT SECTION
			cmct_histogram = cmct.cmct(img_path)
			commons.addFileLine(''+img_path + ',' + (','.join(str(index_value) for index_value in cmct_histogram )) + '\n', cmct_file)
			#ECMCT SECTION
			ecmct_histogram = ecmct.ecmct(img_path)
			commons.addFileLine(''+img_path + ',' + (','.join(str(index_value) for index_value in ecmct_histogram )) + '\n', ecmct_file)
	
	commons.closeFile(lbp_file)
	commons.closeFile(cmct_file)
	commons.closeFile(ecmct_file)
	print('All images are now processed')
if __name__== "__main__":
  main()

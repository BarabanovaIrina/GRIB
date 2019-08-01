import pygrib
import pandas as pd
import os
import os.path

def create_csv():
	drct = './dataset/'

	files = os.listdir('./dataset')
	sorted_files = sorted(files)
	columns=['filename','dataDate','dataTime','P1','yearOfCentury','month','day','hour','minute','numberOfCodedValues','validDate','analDate']
	whole_data = []


	k=0
	for filename in sorted_files:
	    grbs = pygrib.open(drct+filename)
	    for grb in grbs[:1]:
	    	cur_data=[]
	    	cur_data = [filename, grb['dataDate'], grb['dataTime'], grb['P1'], grb['yearOfCentury'], grb['month'],
	                    grb['day'], grb['hour'], grb['minute'], grb['numberOfCodedValues']]

	    	try:
	    		cur_data.append(grb['validDate'])
	    	except RuntimeError:
	    		cur_data.append('validDateKeyError')
	    	try:
	    		cur_data.append(grb['analDate'])
	    	except RuntimeError:
	        	cur_data.append('analDateKeyError')

	    	whole_data.append(cur_data)

	    k+=1
	    if k%10 == 0:
	    	print('{} files passed'.format(k))
	        
	df = pd.DataFrame(whole_data, columns=columns)
	df.to_csv('gribData.csv')

# if __name__ == '__main__':
# 	create_csv()

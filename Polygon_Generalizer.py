# -*- coding: utf-8 -*-
"""
@author: mvenkov
"""
from shapely import geometry as geo
import csv

def load_shapefile(filename):
	with open(filename, 'rb') as csvfile:
		reader=csv.reader(csvfile)
		row_num=0
		column_names=[]
		data=[]

		for row in reader:
			if row_num==0:
				column_names=row
			else:
				data.append(row)
			row_num+=1
		return column_names,data

def table_to_dict(table):
	output={}
	num_set=set()
	dict_row=[]
	polygon=[]
	cur_num=None
	cur_poly='1'
	row_num=0

	for row in table:
		num = row[0]
		prov = row[1]
		poly_num=row[2]
		x=row[3]
		y=row[4]
		path=row[5]

		if row_num==0:
			polygon.append([float(x),float(y)])
			cur_num=num
		elif num==cur_num and poly_num==cur_poly:
			polygon.append([float(x),float(y)])
		elif num==cur_num and poly_num!=cur_poly:
			dict_row.append(polygon)
			cur_poly=poly_num
			polygon=[]
			polygon.append([float(x),float(y)])
		elif num!=cur_num:
			# print 'worked'
			dict_row.append(polygon)
			output[cur_num]={'prov':prov, 
							 'polygons':dict_row}
			cur_num=num
			cur_poly=poly_num
			polygon=[]
			dict_row=[]
			polygon.append([float(x),float(y)])

		row_num+=1

	# Last point to add
	dict_row.append(polygon)
	output[cur_num]={'prov':prov, 
				 'polygons':dict_row}

	return output

def plot_polygon(polygon):
	import matplotlib.pyplot as plt
	print 'Number of coordiantes: ', len(polygon)
	xs = [x[0] for x in polygon]
	ys = [x[1] for x in polygon]
	plt.plot(xs, ys)
	plt.show()

def flatten_dict_and_simplify(input_dict):
	# Converts dictionary into a list that can be saved a CSV file
	print 'Flattening dictionary...'
	num = None
	name = None
	prov = None
	poly_num=0
	coor = []
	output = []
	row=1
	# Full description
	# output.append(['num','name','prov','poly_num','X','Y','Path'])

	# Reduced size
	output.append(['num','prov','poly_num','X','Y','Path'])

	# import pprint
	#pprint.pprint(input_dict)

	for entry in input_dict:
		num = entry
		prov = input_dict[entry]['prov']
		poly_num = 0
		for p in input_dict[entry]['polygons']:
			poly_num+=1
			if len(p)>50:
				try:
					X, Y = simplify_polygon(p)
				except:
					print 'Crashed at'
					print num
					print poly_num
					print p
					# return None
			else:
				X,Y=zip(*p)

			for i in range(len(X)):
				# output.append([num, name, prov,poly_num, X, Y, row])
				# Reduced size:
				output.append([num,prov, poly_num, X[i], Y[i], row])
				row+=1
	print 'Finished flattening'
	return output

def simplify_polygon(polygon):
	from shapely.geometry.polygon import Polygon
	shape = Polygon(polygon)
	# @500 10 fold reduction with good detail
	# @50 virtually no white spaces
	simplified = shape.simplify(500, preserve_topology=True)

	return simplified.exterior.xy


if __name__=='__main__':
	import os
	import pprint as pp
	import matplotlib.pyplot as plt
	from shapely.geometry.polygon import Polygon
	

	wd = os.path.dirname(os.path.realpath(__file__))
	data_dir = os.path.join(wd,'data')
	shape_file=os.path.join(data_dir,'final.csv')

	column_names,data = load_shapefile(shape_file)

	data_dict=table_to_dict(data)

	# test = data_dict['35107']['polygons'][1]
	print data_dict['35107']['prov']
	# plot_polygon(test)
	# xs = [x[0] for x in test]
	# ys = [x[1] for x in test]
	# plt.plot(xs, ys) 

	# x,y = simplify_polygon(test)

	# print 'Pre processing length',len(test)
	# print 'Simplified length',len(x)

	# plt.plot(x,y,color='r')
	# plt.show()

	# Explicitly encode to STR to avoid issues with French letters
	final = flatten_dict_and_simplify(data_dict)



	print 'Writing to file...'
	outfile= os.path.join(data_dir,'final_simplified.csv')
	with open(outfile,'wb') as f:
		writer = csv.writer(f)
		writer.writerows(final)

	print 'Rows written:', len(final)
	print 'End of script'

	

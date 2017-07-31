# -*- coding: utf-8 -*-

import pandas as pd
from sets import Set
from py2oracle import compare_data

'''
class checker():
	def __init__(self, dataframe):
		self.dataframe = dataframe
		if type()
'''

def check_na(dataframe, on_columns=[]):
	'''
	
	Function
	----------
	Check if columns in on_columns contain None. 

	Output
	----------
	The output is a dictionary, users can use 'key' to get specific information:

	1. check_na['result']: True or False
		True: if at least one column contain None.
		False: if none of the columns contain None.
	2. check_na['rows']: dataframe
		The corresponding rows that at least one column in on_columns is None.
	3. check_na['columns']:  list
		The columns names that contain None.

	Parameters
	----------
	dataframe: Dataframe
	on_columns: list
		Column names that being checked. ALl of them should be in dataframe.

	Example
	----------


	'''
	if Set(dataframe.columns).issuperset(Set(on_columns)):
		
		result = []
		na_index = []
		na_columns = []
	
		df = dataframe.reset_index()[on_columns].isnull()
		for col in on_columns:	
			temp = df[col][df[col]==True]	# select a series that is null
			if temp.size>0:
				na_columns.append(col)
				na_index.extend(temp.index.tolist())
			else:
				continue
		
		if len(na_columns)==0:
			result = False	# none of columns contain None
		else:
			result = True	# at least one column contain None

		index = list(Set(na_index))
		return {'result':result, 'columns':na_columns, 'rows':dataframe.iloc[index]}
	else:
		return {'result':'The parameter \'on_columns\' contains the column names that not in dataframe!',
		 'columns':'', 'rows':''}

def check_zero(dataframe, on_columns=[]):
	'''
	Function
	----------
	Check if columns in on_columns contain 0/zero. 

	Output
	----------
	The output is a dictionary, users can use 'key' to get specific information:

	1. check_na['result']: True or False
		True: if at least one column contain 0/zero.
		False: if none of the columns contain 0/zero.
	2. check_na['rows']: dataframe
		The corresponding rows that at least one column in on_columns is 0/zero.
	3. check_na['columns']:  list
		The columns names that contain 0/zero.

	Parameters
	----------
	dataframe: Dataframe
	on_columns: list
		Column names that going be checked 

	Example
	----------

	'''

	if Set(dataframe.columns).issuperset(Set(on_columns)):
		df = dataframe.reset_index()[on_columns]
		
		df = df==0	# check 0/zero
		
		result = []
		zero_index = []
		zero_columns = []

		for col in on_columns:
			temp = df[col][df[col]==True]	# select a series that is 0/zero
			if temp.size>0:
				zero_columns.append(col)
				zero_index.extend(temp.index.tolist())
			else:
				continue

		if len(zero_columns)==0:
			result = False	# none of columns contain 0/zero
		else:
			result = True	# at least one column contain 0/zero

		index = list(Set(zero_index))
		return {'result':result, 'columns':zero_columns, 'rows':dataframe.iloc[index]}
	else:
		return {'result':'The parameter \'on_columns\' contains the column names that not in dataframe!',
		 'columns':'', 'rows':''}

def check_pairs(dataframe, key_columns=[], value_columns=[], keep='first'):
	'''
	Function
	----------
	Check if exist duplicated keys within key-vlaue pairs.

	Output
	----------
	The output is a dictionary, users can use 'key' to get specific information:

	1. check_na['result']: True or False
		True: exist duplicated keys within key-vlaue pairs.
		False: don't exist duplicated keys within key-vlaue pairs.
	2. check_na['rows']: dataframe
		The corresponding rows that have duplicated keys.
	3. check_na['parirs']:  dataframe
		The duplicated key-vlaue pairs.

	Parameters
	----------
	dataframe: Dataframe
	key_columns: list
		Column names that will combine to be the key.
	value_columns: list
	    Column names that will combine to be the value.
	keep: first or last, default 'first'
	     first: delete duplicates rows except for the first occurrence.
	     last: delete duplicates rows except for the last occurrence.

	Example
	----------

	'''

	df = dataframe.drop_duplicates(key_columns+value_columns,keep=keep)
	df_result = df[df.duplicated(key_columns,keep=False)].sort_values(key_columns)

	result = []
	duplicate_pairs = df_result[key_columns+value_columns].reset_index(drop=True)

	if df_result.shape[0] == 0:
		result = True
	else:
		result = False

	return {'result':result,'rows':df_result,'pairs':duplicate_pairs}

def check_outlier(dataframe, on_columns=[], outlier='', how='==', dropna=True):

	df = dataframe.reset_index()[on_columns]

	if how == '==':
		temp = df==outlier
	elif how == '>=':
		temp = df >= outlier
	elif how == '>':
		temp = df > outlier
	elif how == '<=':
		temp = df <= outlier
	else:
		temp = df < outlier

	if dropna:
		return df[temp].dropna()
	else:
		return df[temp]


'''
	for col in on_columns:
		temp = df[col][df[col]==how]
		if temp.size>0:
			na_detail.append([col, temp.size])
			na_columns.append(col)
		else:
			continue
'''

def str_to_list(series, split_by='', strip=True):
	s = series.apply(lambda x: x.encode('utf-8').split(split_by)).tolist()

	if strip:
		s1 = [[i.strip() for i in item] for item in s]

	retult = pd.Series(s1, index=series.index)
	return retult

def check_total(dataframe_1, dataframe_2, sum_cols=[]
				,sum_cols_left=[], sum_cols_right=[], decimal=2):
	
	df_1_total = []
	df_2_total = []
	columns = []
	result = ''

	if len(sum_cols)>0:
		sum_cols_left=sum_cols_right=sum_cols

	if len(sum_cols_left)==len(sum_cols_right):
		for i in xrange(len(sum_cols_left)):
			temp_1 = dataframe_1[sum_cols_left[i]].sum()
			temp_2 = dataframe_2[sum_cols_right[i]].sum()
			df_1_total.append(round(temp_1, decimal))
			df_2_total.append(round(temp_2, decimal))

	for i in xrange(len(sum_cols_left)):
		if df_1_total[i]!=df_2_total[i]:
			columns.append((sum_cols_left[i], sum_cols_right[i]))

	if len(columns)==0:
		result = 'Correct!'
	else:
		result = 'Error!'

	return {'result':result, 'columns':columns}











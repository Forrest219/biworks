# -*- coding: utf-8 -*-

import pandas as pd
from sets import Set

'''
class checker():
	def __init__(self, dataframe):
		self.dataframe = dataframe
		if type()
'''

def check_na(dataframe, on_columns=[], how=True):
	'''
	Check if certain columns is or isn't None. 

	The result is a dictionary, users can use furtuer method to get more information:

	1. check_na[result]：'Correct!' or 'Error!'
		Correst!: if at least one column meet the checking condition;
		Error!: if none of the columns meet the checking condition.
	
	2. check_na[rows]: the corresponding rows(DataFrame) that meet the checking condition;
	3. check_na[columns]: the columns names(list) that meet the checking condition.

	Parameters
	----------
	dataframe: Dataframe
	on_columns: list
		Column names that going be checked 
	how: True or False, default True
		True: if certain columns is None
		False: if certain columns isn't None

	'''
	if Set(dataframe.columns).issuperset(Set(on_columns)):
		result = []
		na_index = []
		na_columns = []

		df = dataframe.reset_index()[on_columns].isnull()
		for col in on_columns:
			# select dataframe that meet the checking condition
			temp = df[col][df[col]==how]
			if temp.size>0:
				na_columns.append(col)
				na_index.extend(temp.index.tolist())
			else:
				continue
		
		if len(na_columns)==0:
			result = 'Correct!'
		else:
			result = 'Error!'

		index = list(Set(na_index))
		return {'result':result, 'columns':na_columns,'rows':dataframe.iloc[index]}
	else:
		return {'result':'The parameter \'on_columns\' contains the column names that not in dataframe!',
		 'columns':'', 'rows':''}

def check_zero(dataframe, on_columns=[], how=True):
	'''
	Check if certain columns contain or not contain zero. 

	The result is a dictionary, users can use furtuer method to get more information:

	1. check_zero[result]：'Correct!' or 'Error!'
		Correst!: if at least one column meet the checking condition;
		Error!: if none of the columns meet the checking condition.
	
	2. check_na[rows]: the corresponding rows(DataFrame) that meet the checking condition;
	3. check_na[columns]: the columns names(list) that meet the checking condition.

	Parameters
	----------
	dataframe: Dataframe
	on_columns: list
		Column names that going be checked 
	how: True or False, default True
		True: if certain columns is zero
		False: if certain columns isn't zero

	'''

	if Set(dataframe.columns).issuperset(Set(on_columns)):
		df = dataframe.reset_index()[on_columns]
		df = df==0
		result = []
		zero_index = []
		zero_columns = []

		for col in on_columns:
			# select dataframe that meet the checking condition
			temp = df[col][df[col]==how]
			if temp.size>0:
				zero_columns.append(col)
				zero_index.extend(temp.index.tolist())
			else:
				continue

		if len(zero_columns)==0:
			result = 'Correct!'
		else:
			result = 'Error!'

		index = list(Set(zero_index))
		return {'result':result, 'columns':zero_columns, 'rows':dataframe.iloc[index]}
	else:
		return {'result':'The parameter \'on_columns\' contains the column names that not in dataframe!',
		 'columns':'', 'rows':''}

def check_key(dataframe, key_columns=[], value_columns=[]):

	duplicate_key = []
	df = dataframe.drop_duplicates(keep='first')[key_column+value_columns]
	df_result = df[df.duplicated(key_column,keep=False)]

	return df_result


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



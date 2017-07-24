# -*- coding: utf-8 -*-
#设置Python读取文件使用的编码utf8（默认为ascii）
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pandas as pd

# check signal table

def check_na(dataframe, on_columns=[], how=True):
	'''
	'''

	df = dataframe.reset_index()[on_columns].isnull()

	na_columns = []
	detail = []

	for col in on_columns:
		temp = df[col][df[col]==how]
		if temp.size>0:
			na_detail.append([col, temp.size])
			na_columns.append(col)
		else:
			continue

	return na_columns

def check_zero(dataframe, on_columns=[], how=True):

	df = dataframe.reset_index()[on_columns]
	df = df==0

	zero_columns = []
	detail = []

	for col in on_columns:
		temp = df[col][df[col]==how]
		if temp.size>0:
			na_detail.append([col, temp.size])
			na_columns.append(col)
		else:
			continue

	return zero_columns

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
	

	return df[temp].dropna()

'''
	for col in on_columns:
		temp = df[col][df[col]==how]
		if temp.size>0:
			na_detail.append([col, temp.size])
			na_columns.append(col)
		else:
			continue
'''



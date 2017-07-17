import pandas as pd

try:	
    from sets import Set    # python 2.x
except ImportError:
    Set = set    # python 3.x

def unpivot(dataframe, index_columns=[], new_columns=['column_name','value'], dropna=True, dropzero=True):
	'''
	unpivot a dataframe with no index by setting index columns

 	Examples
 	--------
 	from biworks import unpivot
	import pandas as pd

	row_data = pd.DataFrame([['one', 'a','1','2'], 
							['one', 'b', None,'4'], 
							['two', 'a','5',0], 
							['two', 'b','7','8']], columns= list('ABCD'))

	print unpivot(row_data, index_columns=['A','B'], dropna=False, dropzero=True)
   
	result:
   ------
        A  B column_name value
	one  a           C     1
	one  a           D     2
	one  b           C  None
	one  b           D     4
	two  a           C     5
	two  b           C     7
	two  b           D     8
	
	'''

	# check if index_columns contains the column names that not in dataframe 
	if Set(dataframe.columns).issuperset(Set(index_columns)):
		df = dataframe.set_index(index_columns).stack(dropna=dropna).reset_index()
		df = df.rename(columns = {'level_'+str(len(index_columns)):new_columns[0], 0:new_columns[1]})
		if dropzero:
			df = df.loc[lambda df: df[new_columns[1]]!=0,:]
		return 	df
	else:
		print 'The parameter \'index_columns\' contains the column names that not in dataframe!'
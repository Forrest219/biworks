# -*- coding: utf-8 -*-
from biworks import unpivot

import pandas as pd

row_data = pd.DataFrame([
	['one', 'a','1','2'], 
	['one', 'b', None,'4'], 
	['two', 'a','5',0], 
	['two', 'b','7','8']],
 columns= list('ABCD'))

print row_data

print unpivot(row_data, index_columns=['A','B'], dropna=False, dropzero=True)
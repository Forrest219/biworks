# -*- coding: utf-8 -*-

#设置Python读取文件使用的编码utf8（默认为ascii）
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import datetime
import pandas as pd

import checker as ch
from py2oracle import connect_db, get_data, connect_close

'''
------setp1：初始化--------
'''

# 1.配置数据库信息，读取配置表数据
print '开始检查数据...\n'
print 'setp1:\n  1.1 加载检查规则配置表...'

bidw_31 = connect_db('31', 'bidw', 'BIDW')
biods_31 = connect_db('31', 'biods', 'BIODS')
bidw_35 = connect_db('35', 'bidw', 'BIDW')
biods_35 = connect_db('35', 'biods', 'BIODS')

py_check = get_data(biods_31, 'select * from py_check')
py_check['ON_COLUMNS'] = ch.str_to_list(py_check.ON_COLUMNS, split_by=',', strip=True)

print '  1.2 加载完毕!\n'


'''
------setp2：核对数据--------
'''

# 2.对指定列进行检查
## 2.1 check_na
print 'setp2:\n  2.1 正在检查缺失值...'

py_check_na = py_check[py_check['CHECK_TYPE']=='check_na']
check_na_result = []

for i in py_check_na.index:	
	row = py_check_na.loc[i]
	db = row.DB_ENVIRONMENT
	table_name = row.TABLE_NAME
	on_columns = [item.upper() for item in row.ON_COLUMNS]
	sql = 'select * from '+table_name
	checking_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') 

	if db == 'bidw_31':
		temp_result = ch.check_na(get_data(bidw_31, sql), on_columns=on_columns)
	elif db == 'biods_31':
		temp_result = ch.check_na(get_data(biods_31, sql), on_columns=on_columns)
	elif db == 'bidw_35':
		temp_result = ch.check_na(get_data(bidw_35, sql), on_columns=on_columns)
	
	check_na_result.append([db, table_name, 'check_na', temp_result['result']
							, temp_result['columns'], checking_time]) 
	
check_na_result = pd.DataFrame(check_na_result, 
								columns=['db','table_name','check_type','check_result'
										 ,'error_columns', 'checking_time'])

#check_na_result.to_excel('check_na.xlsx', sheet_name = 'check_na_'+checking_time
#						, index_label='index')

print '  2.1 缺失值检查完毕.\n'


## 2.1 check_zero
print '  2.2 正在检查零值...'

py_check_zero = py_check[py_check['CHECK_TYPE']=='check_zero']
check_zero_result = []

for i in py_check_zero.index:	
	row = py_check_zero.loc[i]
	db = row.DB_ENVIRONMENT
	table_name = row.TABLE_NAME
	on_columns = [item.upper() for item in row.ON_COLUMNS]
	sql = 'select * from '+table_name

	if db == 'bidw_31':
		temp_result = ch.check_zero(get_data(bidw_31, sql), on_columns=on_columns)
	elif db == 'biods_31':
		temp_result = ch.check_zero(get_data(biods_31, sql), on_columns=on_columns)
	
	check_zero_result.append([db, table_name, 'check_zero', temp_result['result']
							, temp_result['columns'], checking_time]) 
	
check_zero_result = pd.DataFrame(check_zero_result,
								columns=['db','table_name','check_type','check_result'
										,'error_columns', 'checking_time'])

#check_zero_result.to_excel('check_zero.xlsx', sheet_name = 'check_zero_'+checking_time, index_label='index')

print '  2.2 零值检查完毕.\n'


'''
------setp3：导出数据--------
'''

print 'setp3:\n  3.1 正在将核对结果输出到Excel...'

concat_result = pd.concat([check_na_result, check_zero_result], axis=0, ignore_index=True)
concat_result.to_excel('check_result.xlsx', sheet_name = 'check_zero_'+checking_time, index_label='index')

print '  3.2 核对结果已输出！'
print '\n核对结束!\n'
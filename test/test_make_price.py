# -*- coding:utf-8 -*- 
'''
Created on 2015/3/14
@author: Jimmy Liu
'''
import unittest
import tushare.stock.trading as fd
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pandas.io.pytables import HDFStore
from sqlalchemy.types import VARCHAR
import tushare as ts
import pandas as pd
import time

#numArr = 

#ts.get_hist_data('159905') #一次性获取全部日k线数据

#df = ts.get_today_all()
#df = ts.get_hist_data('159905') 
#print(type(df))

#2016/6/6
#2018/12/5

# 选取等于某些值的行记录 用 == 
# # df.loc[df['column_name'] == some_value]

# 选取某列是否是某一类型的数值 用 isin
# # df.loc[df['column_name'].isin(some_values)]

# 多种条件的选取 用 &
# # df.loc[(df['column'] == some_value) & df['other_column'].isin(some_values)]

# 选取不等于某些值的行记录 用 ！=
# # df.loc[df['column_name'] != some_value]

# isin返回一系列的数值,如果要选择不符合这个条件的数值使用~
# # df.loc[~df['column_name'].isin(some_values)]

df=pd.read_csv("../data/510900_sell.csv",encoding="gb18030")

#提取行索引
index = df.index
print(index)
 # 提取列索引
columns = df.columns
print(columns)

row = next(df.iterrows())[1]

print(row['date'])

print(df.loc[df['date']=='2018-12-05'])

row = df.loc[df['date']=='2018-12-05']

print(row['open'])
#print(df.loc[df['date'] == '2018/12/5'])

#print('time.gmtime(): ', time.gmtime())
# 输出：
# time.gmtime():  time.struct_time(tm_year=2018, tm_mon=4, tm_mday=17, tm_hour=7, tm_min=32, tm_sec=54, tm_wday=1, tm_yday=107, tm_isdst=0)
#开始日期
begin = (2018, 4, 17, 15, 20, 12, 1, 107, 0);
print('time.mktime(begin): %f' % time.mktime(begin))
timestamp = time.mktime(begin)

#本金10万
total_money = 100000

step_num = 10000

use_money = 0
take_buck = 0

#获得时间
#print(time.strftime('%Y-%m-%d',time.localtime(timestamp)))

cur_index = time.strftime('%Y-%m-%d',time.localtime(timestamp))
print("cur_index:",cur_index)
row = df.loc[df['date'] == cur_index]

#建立初始仓位
price0 = row['low']

use_money = price0*40000
total_money = total_money - use_money
take_buck = 40000

df_buck = 
	
#86400s
for i in range(1, 30):
	timestamp
	cur_index = time.strftime('%Y-%m-%d',time.localtime(timestamp))
	print("cur_index:",cur_index)
	row = df.loc[df['date'] == cur_index]
	
	
	timestamp= timestamp+86400
	
else:
    print 'The for loop is over' 



#一天86400秒











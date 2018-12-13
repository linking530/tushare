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

df=pd.read_csv("../data/159905.csv",encoding="gb18030")

df_busk=pd.DataFrame(columns={'price','aim_price','aim_all_price','num','total_money','take_buck'})

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
total_money = 200000

use_money = 0
take_buck = 0

#获得时间
#print(time.strftime('%Y-%m-%d',time.localtime(timestamp)))

cur_index = time.strftime('%Y-%m-%d',time.localtime(timestamp))
print("cur_index:",cur_index)
row = df.loc[df['date'] == cur_index]

#建立初始仓位
price0 = 1.16

use_money = price0*3000
total_money = total_money - use_money
take_buck = 3000

#price	num	aim_price	aim_all_price

price = price0

for i in range(-10,10):
	aim_price =  price*1.05
	aim_all_price = price*1.20
 	df_row = pd.DataFrame([[price,aim_price, aim_all_price,0]], columns=['price','aim_price','aim_all_price','num'])
	#print([price,aim_price, aim_all_price,0])
	price = price0*(1+i*0.05)
	df_busk = df_busk.append(df_row,ignore_index=True,sort=True)

df_busk.to_csv("../data/510900_sell.csv",encoding="gb18030")

print(df_busk)


for i in range(1, 300):
	cur_index = time.strftime('%Y-%m-%d',time.localtime(timestamp))
	#print("cur_index:",cur_index)
	#取得当前日期的价格
	row = df.loc[df['date'] == cur_index]
	
	#遍历股票仓位表
	for index_busk, row_busk in df_busk.iterrows():   # 获取每行的index、row
		# print("-------------------------------------")
		# print(type(row_busk['price']))
		# print("-------------------------------------")
		# print(row['high'])
		# print("-------------------------------------")
		# print(row['low'])
		# print("-------------------------------------")
		# print(row['high'].values[0])
		# print("-------------------------------------")
		if row['high'].empty :
			continue
		if  row_busk['price']<row['high'].values[0] and row_busk['price']>row['low'].values[0]:
			buy_num = 5000
			use_money = row_busk['price']*buy_num
			if total_money<use_money:
				buy_num = total_money/row_busk['price']*100
				buy_num = buy_num*100
				
			use_money = row_busk['price']*buy_num	
			total_money = total_money - use_money
			take_buck = take_buck+buy_num
			print('buy:',index_busk,row_busk['price'],buy_num)			
			curnum= df_busk.loc[index_busk,'num']-buy_num	
			df_busk.loc[index_busk,'num']  = curnum
			
	# for index_busk, row_busk in df_busk.iterrows():   # 获取每行的index、row	
		# if  row_busk['aim_price'].item() < row['high'].item() & row_busk['aim_price'].item()>row['low'].item():
			# sell_num = 5000	#基本卖出股数
			# if sell_num.any()<row_busk['num'].any():
				# sell_num = row_busk['num'].astype('float64')
				
			# get_money = row_busk['aim_price']*sell_num	
			# total_money = total_money + get_money
			# take_buck = take_buck-sell_num
			# df_busk.iloc[index_busk,'num'] = df_busk.iloc[index_busk,'num'] -sell_num	
			# print('sell:',row_busk['aim_price'],sell_num)


	timestamp= timestamp+86400
	
else:
    print 'The for loop is over' 





print(total_money)




#一天86400秒

#df_busk.to_csv("../data/510900_sell.csv",encoding="gb18030")




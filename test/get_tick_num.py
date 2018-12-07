# -*- coding:utf-8 -*- 
'''
Created on 2015/3/14
@author: Jimmy Liu
'''
#获得基础数据
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pandas.io.pytables import HDFStore
from sqlalchemy.types import VARCHAR
import tushare as ts

#numArr = 

#ts.get_hist_data('159905') #一次性获取全部日k线数据

#df = ts.get_today_all()
df = ts.get_hist_data('510900') 
#print(type(df))
df.to_csv("../data/510900.csv",encoding="gb18030")


engine = create_engine('mysql://root:root@127.0.0.1/tushare-master?charset=utf8')


df.to_sql('510900',engine,if_exists='replace',dtype={'date':VARCHAR(length=20)})



# print(df.head(1))
# print(df.describe())
# for idx, row in df.iterrows():
    # print idx, row

#		engine = create_engine('mysql://root:jimmy1@127.0.0.1/mystock?charset=utf8')
#     db = 		MySQLdb.connect(host='127.0.0.1',user='root',passwd='jimmy1',db="mystock",charset="utf8")
#     df.to_sql('TICK_DATA',con=db,flavor='mysql')
#     db.close()

# engine = create_engine('mysql://pass@localhost/test'echo=True)
# DBSession = sessionmaker(bind=engine)
# session = DBSession()
# ret=session.execute('desc user')
# print ret
#print ret.fetchall()
# print ret.first()
# mysql://root:pass/test
# root是用户名 pass密码 test数据库
# session相当于MySQLdb里面的游标
# first 相当于fetchone
# echo=True 会输出所有的sql
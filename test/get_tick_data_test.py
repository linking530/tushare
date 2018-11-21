# -*- coding:utf-8 -*- 
'''
Created on 2015/3/14
@author: Jimmy Liu
'''
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pandas.io.pytables import HDFStore
import tushare as ts

df = ts.get_stock_basics()
#print(type(df))
df.to_csv("stock_basics.csv",encoding="gb18030")
# print(df.head(1))
# print(df.describe())
# for idx, row in df.iterrows():
    # print idx, row

    engine = create_engine('mysql://root:root@127.0.0.1/mystock?charset=utf8')
	
#		engine = create_engine('mysql://root:jimmy1@127.0.0.1/mystock?charset=utf8')
#     db = 		MySQLdb.connect(host='127.0.0.1',user='root',passwd='jimmy1',db="mystock",charset="utf8")
#     df.to_sql('TICK_DATA',con=db,flavor='mysql')
#     db.close()
    df.to_sql('tick_data',engine,if_exists='append')
	
	
	

engine = create_engine('mysql://pass@localhost/test'echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
ret=session.execute('desc user')
print ret
# print ret.fetchall()
print ret.first()
mysql://root:pass/test
root是用户名 pass密码 test数据库
session相当于MySQLdb里面的游标
first 相当于fetchone
echo=True 会输出所有的sql
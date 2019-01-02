#-*-coding:utf-8-*-
import requests
import time
#from fake_useragent import UserAgent
import re
import threading
import random
import os
import sys
import codecs
import csv
import sys
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
from bs4 import BeautifulSoup

reload(sys)

sys.setdefaultencoding('utf-8')
#基金列表
fund_list_pd=pd.DataFrame(columns=['id','name'])
achievement_pd=pd.DataFrame(columns=['id','name','近1月','近3月','近6月','近1年','近3年','成立来'])
def get_fund_list():
    """爬取简单的基金代码名称目录"""
    #ua = UserAgent()
    #header = {"User-Agent": ua.random}
    global fund_list_pd
    page = requests.get('http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,'
                        'desc&page=1,9999&feature=|&dt=1536654761529&atfc=&onlySale=0')
                        
    print('fund_list_pd page.encoding:',page.encoding)
    # 基金目录
    fund_list = re.findall(r'"[0-9]{6}",".+?"', page.text)

    # 保存到文件
    fund_save = dict()
    count = 0
    for i in fund_list:
        count += 1
        fund_save[i[1:7]] = i[10:-1]
        #print("No."+str(count)+"  "+i[1:7]+"  "+i[10:-1])	

    for key, value in fund_save.items():
        fund_list_pd = fund_list_pd.append({'id':key, 'name':value}, ignore_index=True)	

    fund_list_pd.to_csv("../data/fund_list.csv",encoding="gb18030")

def get_achievement(code, name,sign):
    global achievement_pd
    print('get_achievement')
    """用于爬取基金的收益率和基金经理的信息"""
    try:
        proxy = random.choice(proxies_http_list)  # 代理ip
        proxy_all = {'http': proxy['ip']}  # 代理ip
    except IndexError:
        proxy_all = None

    if sign > 0:
        #ua = UserAgent()
        #header = {"User-Agent": ua.random}
        try:
            try:
                page = requests.get('http://fund.eastmoney.com/' + code + '.html', headers=header, proxies=proxy_all)
            except:
                try:
                    if proxy_all:
                        if proxy['err_count'] == 5:
                            proxies_http_list.remove(proxy)
                        else:
                            proxy['err_count'] += 1
                except ValueError:
                    pass
                page = requests.get('http://fund.eastmoney.com/' + code + '.html')
                #print('http://fund.eastmoney.com/' + code + '.html')
            page.encoding = 'utf-8'
            print('page.encoding:',page.encoding)
            re_text = page.text
        except Exception as e:
            print(e)
            print(' '+code)
            time.sleep(2)
            re_text = ''

        sign2 = 1

        #print(re_text)                      
        soup=BeautifulSoup(re_text,'lxml')    
        tags=soup.find_all(class_=re.compile("ui-font-middle ui-color-"))
        tagslen = len(tags)
        m1 = m3 = m6 = y1 = y3 = allt ='1'
        #print(tags)
        if tagslen>2 :
            m1=tags[2].string       
        if tagslen>4 :
            m3=tags[4].string
        if tagslen>6 :        
            m6=tags[6].string
        if tagslen>3 :   
            y1=tags[3].string
        if tagslen>5 :   
            y3=tags[5].string
        if tagslen>7 :   
            allt = tags[7].string

        #name =tags[1].string
        
        print(code,m1,m3,m6,y1,y3,allt)       
        #achievement = achievement.append({'id':key, 'name':value}, ignore_index=True)	
        achievement_pd = achievement_pd.append({'id':code, 'name':name,'近1月':m1,'近3月':m3,'近6月':m6,'近1年':y1,'近3年':y3,'成立来':allt}, ignore_index=True)
        #rece=tags[8].string

        # with open('re_text.txt', 'w') as f:
            # f.write(tags.prettify())
        return achievement_pd


def thread_get_past_performance(code, name, thread_index_fund_file_lock, thread_guaranteed_fund_file_lock,):
    """爬取单个基金信息的线程"""
    # 爬取收益、基金经理信息
    tem, sign = get_achievement(code, 3)
    fund_all_msg = [code, name] + tem
    
    print(fund_all_msg)
    
    # 保存文件
    if sign == 1:
        # 指数型/股票型等基金
        f = open('index_fund_with_achievement.csv', 'a')
        thread_index_fund_file_lock.acquire()
        for i in fund_all_msg:
            f.write(i + ',')
        f.write('\n')
        thread_index_fund_file_lock.release()

    elif sign == 0:
        # 保本型基金
        f = open('guaranteed_fund_with_achievement.csv', 'a')
        thread_guaranteed_fund_file_lock.acquire()
        for i in fund_all_msg:
            f.write(i + ',')
        f.write('\n')
        thread_guaranteed_fund_file_lock.release()
    else:
        # 有封闭期的固定收益基金或已终止的基金
        return

    f.close()
    return


def get_past_performance(source_file_name='fund_simple.csv'):
    """在简单基金目录的基础上，爬取所有基金的信息"""
    # 测试文件是否被占用，并写入列索引
    try:
        if source_file_name == 'fund_simple.csv':
            with open('index_fund_with_achievement.csv', 'w') as f:
                f.write('基金代码,基金名称,近1月收益,近3月收益,近6月收益,近1年收益,近3年收益,成立来收益,基金经理,'
                        '本基金任职时间,本基金任职收益,累计任职时间,\n')
            with open('guaranteed_fund_with_achievement.csv', 'w') as f:
                f.write('基金代码,基金名称,近1月收益,近3月收益,近6月收益,近1年收益,近3年收益,保本期收益,基金经理,'
                        '本基金任职时间,本基金任职收益,累计任职时间,\n')
    except:
        print('文件index_fund_with_achievement.csv或者文件guaranteed_fund_with_achievement.csv无法打开')
        return

    with open(source_file_name, 'r') as f:
        # 线程集合和保存信息文件的线程安全锁
        thread = []
        thread_index_fund_file_lock = threading.Lock()
        thread_guaranteed_fund_file_lock = threading.Lock()

        # 逐个爬取所有基金的信息
        count = 0
        fund_list = f.readlines()
        fund_list_length = len(fund_list)
        for i in fund_list:
            count += 1
            try:
                code, name, _ = i.split(',')
            except ValueError:
                break
            # 多线程爬取
            t = threading.Thread(target=thread_get_past_performance, args=(code, name, thread_index_fund_file_lock
                                                                           , thread_guaranteed_fund_file_lock))
            thread.append(t)
            t.start()
            time.sleep(0.2)
            for t in thread:
                if not t.is_alive():
                    thread.remove(t)

            # 判断线程集合是否过大
            while len(thread) > 10:
                time.sleep(1)
                for t in thread:
                    if not t.is_alive():
                        thread.remove(t)
            print(str(count)+'/'+str(fund_list_length))

    # 等待所有线程执行完毕
    while len(thread) > 0:
        time.sleep(2)
        for t in thread:
            if not t.is_alive():
                thread.remove(t)
        print("the len of thread " + str(len(thread)))
    return


def no_data_handle(fund_with_achievement):
    """对第一次爬取失败的基金信息的重新爬取"""
    # 文件以a方式写入，先进行可能的文件清理
    try:
        os.remove('fund_need_handle.csv')
    except FileNotFoundError:
        pass
    try:
        os.remove('tem.csv')
    except FileNotFoundError:
        pass

    sign = 1
    with open(fund_with_achievement, 'r') as f1:
        print('Handling '+fund_with_achievement)
        for i in f1.readlines():
            # 逐条检查基金信息
            try:
                code, name, one_month, three_month, six_month, one_year, three_year, from_st, _, this_tenure_time, \
                this_return, all_tenure_time, _ = i.split(',')
            except ValueError:
                #code, name, *_ = i.split(',')
                code, name = i.split(',')
                one_month = '-'

            # 当基金信息为未知时(??)
            if one_month == '-':
                sign = 0
                with open('fund_need_handle.csv', 'a') as f2:
                    f2.write(code+','+name+','+'\n')
                continue
            with open('tem.csv', 'a') as f3:
                f3.write(i)

    # 用筛选过的文件替换原来的基金信息文件，并调用函数对信息未知的基金进行重爬
    os.remove(fund_with_achievement)
    os.renames('tem.csv', fund_with_achievement)
    if sign == 0:
        get_past_performance(source_file_name='fund_need_handle.csv')
        os.remove('fund_need_handle.csv')


def get_time_from_str(time_str):
    """将文字描述的任职时间转为列表"""
    tem = re.search('(?:(\d)年又|)(\d{0,3})天', time_str).groups()
    tem_return = list()
    for i in tem:
        if i:
            tem_return.append(int(i))
        else:
            tem_return.append(0)
    # [int(多少年),int(多少天)]
    return tem_return


def data_analysis(fund_with_achievement, choice_cretertion_return, choice_cretertion_time):
    """按传入的训责策略，筛选出符合要求的基金"""
    # 文件以a方式写入，先进行可能的文件清理
    try:
        os.remove('fund_choice.csv')
    except FileNotFoundError:
        pass

    try:
        with open('fund_choice.csv', 'w') as f:
            f.write('基金代码,基金名称,近1月收益,近3月收益,近6月收益,近1年收益,近3年收益,成立来收益/保本期收益,基金经理,'
                    '本基金任职时间,本基金任职收益,累计任职时间,\n')

        with open(fund_with_achievement, 'r') as f:
            count = 0
            for i in f.readlines()[1:]:
                # 逐条检查
                count += 1
                sign = 1

                # 取基金信息，并按收益率和任职时间分类
                _, _, one_month, three_month, six_month, one_year, three_year, from_st, _, this_tenure_time,\
                this_return, all_tenure_time,_ = i.split(',')
                return_all = [one_month, three_month, six_month, one_year, three_year, from_st, this_return]
                time_all = [this_tenure_time, all_tenure_time]

                # 信息未知或一月数据不存在（成立时间过短）的淘汰
                if one_month == '??' or one_month == '--':
                    continue

                # 收益率部分的筛选
                for j, k in zip(choice_cretertion_return.values(), return_all):
                    if k == '--':
                        continue
                    if float(k[:-1]) < j:
                        sign = 0
                        break

                # 任职时间部分的筛选
                if sign == 1:
                    for j, k in zip(choice_cretertion_time.values(), time_all):
                        for l, m in zip(j, get_time_from_str(k)):
                            if m > l:
                                break
                            elif m == l:
                                continue
                            else:
                                sign = 0
                                break

                # 符合要求的保存进文件
                if sign == 1:
                    with open('fund_choice.csv', 'a') as f2:
                        f2.write(i)
                print(count)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    get_fund_list()

    # 打开保存在proxies_http.txt的http代理ip
    proxies_http_list = list()
    # with open('proxies_http.txt', 'r') as f:
    #     for i in f.readlines()[1:]:
    #         tem = {'ip': i[:-1], 'err_count': 0}
    #         proxies_http_list.append(tem)
    
    get_achievement('270045','-',3)
    print(fund_list_pd)
    for index_busk, row_busk in fund_list_pd.iterrows():   # 获取每行的index、row
        # if row_busk['id'].empty :
            # continue
        get_achievement(row_busk['id'],row_busk['name'],3)
        time.sleep(5)    
        achievement_pd.to_csv("../data/achievement_pd.csv",encoding="gb18030")    
    #get_past_performance()
    print(achievement_pd)
    #no_data_handle('index_fund_with_achievement.csv')
    #no_data_handle('guaranteed_fund_with_achievement.csv')

    #对基金的筛选设置
    # choice_cretertion_return = {'近1月收益': 1.60, '近3月收益': -5.36, '近6月收益': 0, '近1年收益': 0,
                                # '近3年收益': -3.30
        # , '成立来收益/保本期收益': 0, '本基金任职收益': 0}
    # choice_cretertion_time = {'本基金任职时间': [1, 0], '累计任职时间': [3, 0]}

    #筛选后的文件为fund_choice.csv，不可修改，若还需要对保本型基金进来筛选，需要先备份
    # data_analysis('index_fund_with_achievement.csv', choice_cretertion_return, choice_cretertion_time)

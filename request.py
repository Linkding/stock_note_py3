# -*- coding: utf-8 -*- 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from sqlalchemy import create_engine
import datetime 
import time
import sys

def get_today():
    today = datetime.date.today()
    return today

def get_yeild_data(start,end):
    url = 'http://yield.chinabond.com.cn/cbweb-pbc-web/pbc/historyQuery?startDate=%s&endDate=%s&gjqx=0&qxId=hzsylqx&locale=cn_ZH' % (start,end)
    header = {
        "Host": "yield.chinabond.com.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "http://yield.chinabond.com.cn/cbweb-pbc-web/pbc/historyQuery?startDate=2019-03-15&endDate=2019-03-15&gjqx=0&qxId=hzsylqx&locale=cn_ZH",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7",
        "Cookie": "JSESSIONID=0000p6U7Rom2sSKLTUElhYwV7HI:-1",
    }
    #从接口获取原始数据
    r = requests.get(url,headers=header)
    # 提供soup处理提取
    soup = BeautifulSoup(r.text)
    ## 预处理，获取html所有tr节点
    length = len(soup.find_all('tr')) 
    l = [] #存储预处理的处理的节点数据，缩小清洗范围
    f = 0
    all_tr = soup.find_all('tr')
    while f < length:
        for i in all_tr[f]:
            if i.string == '中债国债收益率曲线':
                l.append(all_tr[f])
                continue
        f = f+1
    ## 抽取目标数据
    l_len = len(l)
    arr = {'date':[],'10y':[]} ## 定义数据结构，便于转成datafram
    i = 0 
    while i < l_len:
        row = l[i].contents
        row2 = row[3].string
        row3 = row[17].string
        arr['date'].append(row2)
        arr['10y'].append(row3)
        i = i + 1

    return arr ## 返回抽取的结果

def to_sql(start,end):
    res = get_yeild_data(start,end)
    data = pd.DataFrame(data=res)
    engine = create_engine("mysql+pymysql://root:123456@127.0.0.1/stock_note?charset=utf8", encoding="utf-8", echo=True)
    try:
        data.to_sql('gov_bond_yield',engine,if_exists='append',index=False)
        print ('insert  data to gov_bond_yield  success!!')
    except Exception as e:
        print (e)
        print ('insert  data to gov_bond_yield  fail!!')

def main():
    today = get_today()
    # to_sql(today,today)
    arg = sys.argv
    l = len(arg)
    if l == 3: #两个传参
        to_sql(arg[1],arg[2])        
    elif l == 2:  #一个传参
        to_sql(arg[1],arg[1])
    elif l == 1: #0传参
        to_sql(today,today)
    else:     # 超过2个传参
        print ('error: out of argv needed')
    

    
if __name__ == '__main__':
    main()   

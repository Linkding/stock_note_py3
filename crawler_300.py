# -*- coding: utf-8 -*-
import tushare as ts
import datetime
import time
from sqlalchemy import create_engine
import pandas as pd
import sys

ts.set_token('cdfe3ce3a8717b588f35f80a39d239ea4f56e224fd6163d4a3568e4b')
pro = ts.pro_api()
engine = create_engine("mysql+pymysql://root:lfzs@efun.com@127.0.0.1/stock_note?charset=utf8", encoding="utf-8", echo=True)


def get_300(start,end):
    df = pro.index_daily(ts_code='000300.SH',start_date=start, end_date=end,fields='ts_code,trade_date,close,open,high,low')
    engine = create_engine("mysql+pymysql://root:123456@127.0.0.1/stock_note?charset=utf8", encoding="utf-8", echo=True)
    df.to_sql('hs300',engine,if_exists='append',index=False)

def get_stock_data(code,start,end):
    if (code.startswith('6')):
        code = code + '.SH'
    else:
        code = code + '.SZ'
    print ('the code is ',code,'start is ',start,'end is ',end)
    df = pro.daily(ts_code=code,start_date=start, end_date=end,fields='ts_code,trade_date,close,open,high,low')
    print (df)
    # engine = create_engine("mysql+pymysql://root:lfzs@efun.com@127.0.0.1/stock_note?charset=utf8", encoding="utf-8", echo=True)
    df.to_sql('main_stock',engine,if_exists='append',index=False)

def get_base_stock():
    df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    df.to_sql('base_stock',engine,if_exists='append',index=False)

def main():
    # today = datetime.date.today().strftime('%Y%m%d')
    # arg = sys.argv
    # l = len(arg)
    # if l == 4: #两个传参，获取一个时间周期
    #     # get_300(arg[1],arg[2])        
    #     get_stock_data(arg[1],arg[2],arg[3])        
    # elif l == 3:  #一个传参，获取某一天数据
    #     # get_300(arg[1],arg[1])
    #     get_stock_data(arg[1],arg[2],arg[2])
    # elif l == 2: #0传参，默认获取当天数据
    #     # get_300(today,today)
    #     get_stock_data(today,today)
    # else:     # 超过2个传参
    #     print ('error: out of argv needed')
    get_base_stock()

if __name__ == '__main__':
    main()
# coding: utf-8

import tushare as ts
import pandas as pd
import json
from flask import request
from flask import jsonify
from datetime import timedelta, datetime
from sqlalchemy import create_engine
from . import main
import pymysql
from ..api import main as api
from ..api import helper

# 打开数据库连接
db = pymysql.connect("127.0.0.1", "root", "lfzs@efun.com", "stock_note", charset='utf8')
# 使用cursor()方法获取操作游标 
cursor = db.cursor(pymysql.cursors.DictCursor)

#设置ts的token
ts.set_token('cdfe3ce3a8717b588f35f80a39d239ea4f56e224fd6163d4a3568e4b')
pro = ts.pro_api()


def get_date():
    #获取当前日期
    d=datetime.now() #获取当前周几，如果是周末需要往前获取周五的日期
    # 判断逻辑：1、是否周六日；2、是否周一；3、是否16点前后
    if (d.weekday() == 6):  #周日
        today = (datetime.today() + timedelta(-2)).strftime('%Y%m%d')
        return today
    elif (d.weekday() == 5):  #周六
        today = (datetime.today() + timedelta(-1)).strftime('%Y%m%d')
        return today
    elif (d.hour > 16 ):
        today = datetime.today().strftime('%Y%m%d')
        return today
    elif (d.weekday() == 0 and d.hour <= 15 ):  #周一
        today = (datetime.today() + timedelta(-3)).strftime('%Y%m%d')
        return today
    elif (d.hour <= 15 ):
        today = (datetime.today() + timedelta(-1)).strftime('%Y%m%d')
        return today
    else:
        today = datetime.today().strftime('%Y%m%d')
        return today




@main.route('/todo/api/v1.0/tasks', methods=['POST'])
def meg():
    today = get_date()
    #获取当前日期
    # print "d.hour %d " % d.hour
    data = request.get_json()
    print (data)
    print ("today is ",today)
    stock_list = []
    for code in data:
        if (code.startswith('6')):
            code = code + '.SH'
        else:
            code = code + '.SZ'
        df = pro.daily(ts_code=code, trade_date=today)
        a = 1 #设点一循环起始值
        while (df.empty):
            day = (datetime.today() + timedelta(-a)).strftime('%Y%m%d')
            df = pro.daily(ts_code=code,trade_date=day)
            a = a + 1
        df= df.iloc[[-1]]
        stock_list.append(df)
    stock_pd = pd.concat(stock_list)
    print (stock_pd)
    return stock_pd.to_json(orient='records')

# 统计沪深比例
# @main.route('/todo/api/v1.0/tasks', methods=['POST'])
# def get_hs_rate():
#     #获取前端发送过来的股票列表
#     data = request.get_json()
#     #统计深户分类
#     for code in data:
#         if (code.startswith('6')):
#             code = code + '.SH'
#         else:
#             code = code + '.SZ'
#         sql = 'select * from base_stock where ts_code=%s' % code
#         cursor.execute(sql)
#         res = cursor.fetchall()
         
        




@main.route('/', methods=['POST', 'GET'])
@main.route('/todotest/api/v1.0/tasks', methods=['POST', 'GET'])
def meg_test():
    stock_num = ['601601', '600519', '002039', '000568', '600236']
    stock_list = []
    for code in stock_num:
        df = ts.get_k_data(code, ktype='5')
        df = df.iloc[[-1]]
        stock_list.append(df)
    stock_pd = pd.concat(stock_list)
    return stock_pd.to_json(orient='records')

@main.route('/todo/api/v1.0/tasks/<code>', methods=['POST','GET'])
def meg_single(code):
    codes = str(code)
    stock_list = []
    df = ts.get_k_data(codes, ktype='5')
    df = df.iloc[[-1]]
    stock_list.append(df)
    stock_pd = pd.concat(stock_list)
    return stock_pd.to_json(orient='records')

# 从tushare接口获取股票日交易信息存入本地数据库
@main.route('/todo/api/v1.0/tasks/add_new', methods=['POST'])
def add_new_stock():
    data = request.get_json()
    get_new_stock_from_ts(data)
    return json.dumps({"success":"True"})

def get_new_stock_from_ts(data,day=None):
    #默认获取当前日期
    if day is None:
        day = get_date()
    print (data)
    print ("day is ",day)
    for code in data:
        if (code.startswith('6')):
            code = code + '.SH'
        else:
            code = code + '.SZ'
        print (code)
        df = pro.daily(ts_code=code, trade_date=day)
        a = 1 #设点一循环起始值
        # 如果停牌等原因，股价并没有数据，日期倒推，至找到数据为止
        while (df.empty):
            day = (datetime.today() + timedelta(-a)).strftime('%Y%m%d')
            df = pro.daily(ts_code=code,trade_date=day)
            a = a + 1
        engine = create_engine("mysql+pymysql://root:lfzs@efun.com@127.0.0.1/stock_note?charset=utf8", encoding="utf-8", echo=True)
        df.to_sql('main_stock',engine,if_exists='append',index=False)
    
# 获取股票最新股价信息，提供前端获取
@main.route('/todo/api/v1.0/tasks/stock_info', methods=['POST'])
def get_stock():
    #获取当前日期
    today = get_date()
    data = request.get_json()
    print (data)
    print ("today is ",today)
    stock_list = []
    for code in data:
        if (code.startswith('6')):
            code = code + '.SH'
        else:
            code = code + '.SZ'
        print (code)
        res = api.read('main_stock',{
            "where":{
                "ts_code":code,
                "trade_date":today
            }
        })
        # 如果停牌等原因，股价并没有数据，日期倒推，至找到数据为止
        a = 1 #设点一循环起始值
        while (len(res)==0):
            day = (datetime.today() + timedelta(-a)).strftime('%Y%m%d')
            res = api.read('main_stock',{
                "where":{
                    "ts_code":code,
                    "trade_date":day
                }
            })
            a = a + 1
        stock_list.append(res[0])
    print (stock_list)
    return api.respose(stock_list)

# 每日获取股票数据接口，已通过curl定时任务来获取
@main.route('/todo/api/v1.0/tasks/auto_get_stock', methods=['POST'])
def auto_get_stock():
    #从mock获取股票信息
    all_stock = helper.merge_mock('stock')
    print (all_stock)
    stock_code = []
    for i in all_stock:
        stock_code.append(i['code'])
    stock_code = list(set(stock_code)) #去重
    stock_code.remove('999999') #去除现金代码
    print (request.data)
    #获取日期
    if not request.data:
        today = get_date()
    elif 'date' in request.get_json():
        data = request.get_json()
        today = data['date']
    print ('today',today)
    get_new_stock_from_ts(stock_code,today)
    return api.respose({"success":"Ture"})

@main.route('/todo/api/v1.0/tasks/check_stock_code', methods=['POST'])
def check_stock_code():
    data = request.get_json()
    sql = sql = 'select * from base_stock where symbol like="%s%s%s" limit 5'  % ('%',data['code'],'%')
    res = api.exec_sql(sql)
    return api.respose(res)

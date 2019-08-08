# -*- coding: utf-8 -*-
from flask import request
from flask import jsonify
from . import api
import json

import pymysql
# 打开数据库连接
db = pymysql.connect("127.0.0.1", "root", "lfzs@efun.com", "stock_note", charset='utf8')
# 使用cursor()方法获取操作游标 
cursor = db.cursor(pymysql.cursors.DictCursor)


@api.route('/api/v1/<table_name>/<action>',methods=['POST'])
def parse_request(table_name,action):
    print ("table_name:  %s " % table_name)
    print ("action:  %s " % action)
    # print ('re_data:',request.data)
    # print (type(request))
    print (request.data)
    print (request.get_json())
    # 前端传参需要预处理，空参数需要预设个固定变量，再传给处理函数
    if not request.data:
        parser = None
        print ('parser is None')
    else:
        parser = request.get_json()
        print ('parser is gived')
    
    # 将前端参数提交处理函数
    if (action == 'read'):
        result = read(table_name,parser)

    if (action == 'create'):
        result =  create(table_name,parser)
        
    # 回调前端   
    result = respose(result)
    # print (type(rsesult))
    # 关闭游标
    cursor.close()
    # 关闭连接
    db.close()
    return result

# 回调前端
def respose(data):
    res = data
    print (res)
    return jsonify(res)

# 解析post传参
def parse_body(parser):
    result = {}
    # 解析where部分
    if "where" in parser:
        where = 'where '
        for i in parser['where']:
            where =  where + ' ' + i + '=' + "'%s'"  % parser['where'][i] + ' and'
        where = where.rstrip('and')
        result['where'] = where
    else:
        result['where'] = ''

    # 解析limit部分
    if "limit" in parser:
        result['limit'] = parser['limit']
    else:
        result['limit'] = 5
    # 解析by
    if "by" in parser:
        result['by'] 
    return result

# 数据库操作  <读>
def read(table_name,parser=None):
    print ('this is  ',parser)
    parse = parse_body(parser)
    print (parse)
    # print ("limit: %s" % parse['limit'])
    cursor.execute('select * from %s %s limit %s' % (table_name,parse['where'],parse['limit']))
    results = cursor.fetchall()
    return results

# 数据库操作 <写>
def create(table_name,parser):
    key = parser.keys()
    val = list(parser.values())
    
    # 处理key、value便于拼接insert语句
    key = ','.join(key)
    val = json.dumps(val)
    val = val.encode('utf8').decode('unicode_escape')
    val = val.lstrip('[')
    val = val.rstrip(']')
    

    sql = "insert into %s(%s) values (% s)" % (table_name,key, val)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        result = [{"status":"success"}]
        return result
    except:
        # Rollback in case there is any error
        db.rollback()
        result = [{"status":"fail"}]
        return result

def update(table_name,parse):
    pass

def delete(table_name,parse):
    pass

# 提供直接定制sql的接口
def exec_sql(sql):
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
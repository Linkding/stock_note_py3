# -------------------------------------------------------------------------------
# Script_name  : test_tu.py
# Revision     : 1.0
# Date         : 2019-07-18 12:46:42
# Author       : Linkding
# Email        : 619216759@qq.com
# Description  : 
# -------------------------------------------------------------------------------
# -*- coding: utf-8 -*-

import tushare as ts
ts.set_token('cdfe3ce3a8717b588f35f80a39d239ea4f56e224fd6163d4a3568e4b')
pro = ts.pro_api()

df = pro.daily(ts_code='000001.SZ', trade_date='20190717')
print (df)
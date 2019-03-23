#!/bin/bash
for i in {2006..2019}
do
start=${i}-01-01
end=${i}-12-31
/export/py-3.5.6/env/bin/python  /export/stock_notes_py3/request.py $start $end
done
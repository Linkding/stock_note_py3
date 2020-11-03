import requests
import json
import time
import base64

s = requests.session()
s.keep_alive = False

APP_KEY = 'af9f36c4e5c171d1c2d7b5076030d238ca23a82bab5ab3aa59197401aa1504c6'
current_milli_time = lambda: int(round(time.time() * 1000))
timestampe = str(current_milli_time())
signature = base64.b64encode((APP_KEY+timestampe).encode())

header = {
    "BIAO-MOCK-APP-KEY": APP_KEY,
    "BIAO-MOCK-TIMESTAMP":timestampe,
    "BIAO-MOCK-SIGNATURE":signature,
    "Content-Type": "application/json"
}

baseurl = 'https://mock.biaoyansu.com/api/1/'
def mock(url,data=None):
    res = requests.post(url=baseurl+url,headers=header,data=json.dumps(data))
    return res.json()
    # print (res.text)


def creat_singe():
    pass
from flask import render_template
from . import main
import requests
import json

baseurl = 'http://119.29.72.177:8888/api/v1/'
def http(url,data=None):
    res = requests.post(url=baseurl+url,data=json.dumps(data))
    return res.json()
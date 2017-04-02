#encoding=utf-8
# -*- coding:gb2312 -*-

import urllib
import urllib.request
import http.cookiejar
import re
from bs4 import BeautifulSoup
from classifier import Classifier

checkUrl = "http://jwgl.buct.edu.cn/CheckCode.aspx"
postUrl = "http://jwgl.buct.edu.cn/default2.aspx"

# 创建带 cookie 功能的 handler
cookie = http.cookiejar.LWPCookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler, urllib.request.HTTPHandler)
urllib.request.install_opener(opener)

username = '2013012433'
password = 'zhn1106'

picture = opener.open(checkUrl).read()
with open('check.gif','wb') as f:
    f.write(picture)

classifier = Classifier()
classifier.loadTrainingMat()
secretcode = classifier.recognizer("check.gif")

postdata = {
    '__VIEWSTATE': 'dDwyODE2NTM0OTg7Oz7Au3GhNlfrriMFSCY1HWTKgq5dKA==',
    'txtUserName': username,
    'TextBox2': password,
    'txtSecretCode': secretcode,
    'RadioButtonList1': '学生',
    'Button1': '',
    'lbLanguage': '',
    'hidPdrs': '',
    'hidsc': '',
        }

headers = {
    'Host': 'jwgl.buct.edu.cn',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://jwgl.buct.edu.cn/(dxzmap55hhkiw4jte53vdi45)/default2.aspx',
    #'Cookie': cookie,
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Request': '1',
        }

postdata = urllib.parse.urlencode(postdata).encode('utf-8')
request = urllib.request.Request(postUrl, postdata, headers)

try:
    response = opener.open(request)
    result = response.read().decode('gb2312')
    print(response.geturl())
    print(result)
    print(response.getcode())

except urllib.request.HTTPError as e:
    print(e.code)

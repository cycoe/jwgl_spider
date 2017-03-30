#!/usr/bin/python

class Spider(object):
    def __init__(self):
        self.checkUrl = "http://jwgl.buct.edu.cn/CheckCode.aspx"
        self.postUrl = "http://jwgl.buct.edu.cn/default2.aspx"
        self.username = '2013012433'
        self.password = 'zhn1106'

    def formatPostData(self):
        """
        格式化 post 和 headers 键值对
        """
        import urllib
        import urllib.request
        postdata = {
            '__VIEWSTATE': 'dDwyODE2NTM0OTg7Oz7Au3GhNlfrriMFSCY1HWTKgq5dKA==',
            'txtUserName': self.username,
            'TextBox2': self.password,
            'txtSecretCode': self.secretcode,
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
        request = urllib.request.Request(self.postUrl, postdata, headers)
        return request

    def login(self):
        """
        登录教务网，使用 urllib 的 cookie 登录功能
        """
        import urllib.request
        import http.cookiejar
        import re
        from classifier import Classifier

        # 创建带 cookie 功能的 opener
        cookie = http.cookiejar.LWPCookieJar()
        handler = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(handler, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)

        # 抓取验证码，存储 cookie 对象
        picture = opener.open(self.checkUrl).read()
        with open('check.gif','wb') as f:
            f.write(picture)
        # 实例化验证码识别器对象，识别验证码
        classifier = Classifier()
        classifier.loadTrainingMat()
        self.secretcode = classifier.recognizer("check.gif")

        try:
            response = opener.open(self.formatPostData())
            responseUrl = response.geturl()
            if not re.search(self.username, responseUrl):
                raise VerifyError("Wrong Verification code!")
            else:
                result = response.read().decode('gb2312')
                print("login successfully!")
        except urllib.request.HTTPError as e:
            print(e.code)
            exit(0)
        except VerifyError as e:
            print(e)
            print("retry...")
            self.login()

class VerifyError(Exception):
    def __init__(self, errorInfo):
        Exception.__init__(self)
        self.errorInfo = errorInfo
    def __str__(self):
        return self.errorInfo

def main():
    spider =Spider()
    spider.login()

if __name__ == "__main__":
    main()

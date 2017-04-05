#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from requests import Session, Request, exceptions


class Spider(object):
    def __init__(self):
        self.verifyCodeUrl = "http://jwgl.buct.edu.cn/CheckCode.aspx"   #验证码获取地址
        self.jwglLoginUrl = "http://jwgl.buct.edu.cn/default2.aspx"     #教务网登录地址
        self.getGradeUrl = "http://jwgl.buct.edu.cn/xscjcx.aspx"        #成绩获取地址
        self.getScheduleUrl = "http://jwgl.buct.edu.cn/xskbcx.aspx"     #课程表获取地址
        self.postClassUrl = "http://jwgl.buct.edu.cn/xsxk.aspx"         #选课地址
        self.studentID = '2013012433'#学号
        self.username = '朱浩南'#姓名
        self.jwglPassword = 'zhn1106'#教务网密码
        self.major = '0202高分子材料与工程'

        self.session = requests.Session()       #实例化 session 对象
        self.response = self.session.send(self.prepareJwglFirst(), timeout=5)   # GET 方法获取登录网站的 '__VIEWSTATE'

        # 实例化验证码识别器对象
        from classifier import Classifier
        self.classifier = Classifier()
        self.classifier.loadTrainingMat()

        self.remainList = [0, 1, 3, 4, 6, 7, 8, 10, 11, 12, 14]

    def formatHeaders(self, referer=None):
        """
        生成请求的 headers，referer 参数的默认值为 None
        若 referer 为 None，则 headers 不包括 referer 参数
        """
        headers = {
            'Host': 'jwgl.buct.edu.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Request': '1',
            }
        if referer:
            headers['Referer'] = referer
        return headers

    def getVIEWSTATE(self):
        """
        正则获取登录页面的 "__VIEWSTATE"
        """
        import re
        return re.findall('<.*name="__VIEWSTATE".*value="(.*)?".*/>', self.response.text)[0]

    def prepareJwglFirst(self):
        headers = self.formatHeaders()
        req = Request('GET', self.jwglLoginUrl, headers=headers)
        return self.session.prepare_request(req)

    def prepareJwglLogin(self):
        """
        实例化登录 jwgl 需要的 request
        """
        postdata = {
            '__VIEWSTATE': self.getVIEWSTATE(),     #此参数非常重要，通过函数从当前网页源代码获取
            'txtUserName': self.studentID,
            'TextBox2': self.jwglPassword,
            'txtSecretCode': self.verCode,
            'RadioButtonList1': '学生',
            'Button1': '',
            'lbLanguage': '',
            'hidPdrs': '',
            'hidsc': '',
        }
        headers = self.formatHeaders(self.jwglLoginUrl)
        req = Request('POST', self.jwglLoginUrl, headers=headers, data=postdata)
        return self.session.prepare_request(req)

    def prepareGetGrade(self):
        headers = self.formatHeaders(self.response.url)
        params = {
            'xh': self.studentID,
            'xm': self.username,
            'gnmkdm': 'N121605',
        }
        req = Request('GET', self.getGradeUrl, headers=headers, params=params)
        return self.session.prepare_request(req)

    def preparePastGrade(self):
        headers = self.formatHeaders(self.response.url)
        params = {
            'xh': self.studentID,
            'xm': self.username,
            'gnmkdm': 'N121605',
        }
        postdata = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.getVIEWSTATE(),         #此参数非常重要，通过函数从当前网页源代码获取
            'hidLanguage': '',
            'ddlXN': '',
            'ddlXQ': '',
            'ddl_kcxz': '',
            'btn_zcj': '历年成绩',
        }
        req = Request('POST', self.getGradeUrl, headers=headers, params=params, data=postdata)
        return self.session.prepare_request(req)

    def prepareSchedule(self):
        headers = self.formatHeaders(self.response.url)
        params = {
            'xh': self.studentID,
            'xm': self.username,
            'gnmkdm': 'N121603',
        }
        req = Request('GET', self.getScheduleUrl, headers=headers, params=params)
        return self.session.prepare_request(req)

    def preparePastSchedule(self, xn_, xq_):
        headers = self.formatHeaders(self.response.url)
        params = {
            'xh': self.studentID,
            'xm': self.username,
            'gnmkdm': 'N121603',
        }
        postdata = {
            '__EVENTTARGET': 'xnd',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.getVIEWSTATE(),         #此参数非常重要，通过函数从当前网页源代码获取
            'xnd': xn_,
            'xqd': xq_,
        }
        req = Request('POST', self.getScheduleUrl, headers=headers, params=params, data=postdata)
        return self.session.prepare_request(req)

    def prepareClass(self):
        headers = self.formatHeaders(self.response.url)
        params = {
            'xh': self.studentID,
            'xm': self.username,
            'gnmkdm': 'N121101',
        }
        req = Request('GET', self.postClassUrl, headers=headers, params=params)
        return self.session.prepare_request(req)

    def prepareGetClass(self):
        headers = self.formatHeaders(self.response.url)
        params = {
            'xh': self.studentID,
            'xm': self.username,
            'gnmkdm': 'N121101',
        }
        postdata = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.getVIEWSTATE(),         #此参数非常重要，通过函数从当前网页源代码获取
            'DrDl_Nj': self.studentID[:4],
            'zymc': self.major + '主修专业||' + self.studentID[:4],
            'xx': '',
            'Button5': '本专业选课'
        }
        req = Request('POST', self.postClassUrl, headers=headers, params=params, data=postdata)
        return self.session.prepare_request(req)

    def jwglLogin(self, tryNum=10):
        """
        教务网登录函数
        tryNum --> 尝试登录的最大次数，防止因递归深度过大导致溢出
        """
        import re
        tryNum -= 1
        if tryNum < 0:
            print('\n*** stack overflow! exiting...')
            exit(0)

        codeImg = self.session.get(self.verifyCodeUrl, timeout=5)       #获取验证码图片
        with open('check.gif', 'wb') as fr:                             #保存验证码图片
            for chunk in codeImg:
                fr.write(chunk)
        self.verCode = self.classifier.recognizer("check.gif")          #识别验证码

        try:
            self.response = self.session.send(self.prepareJwglLogin(), timeout=5)
            if re.search(self.studentID, self.response.url):            #若 response.url 中匹配到学号，则认为登录成功
                print("login successfully!")
                print(self.response.url)
            else:
                raise VerifyError("Wrong Verification code!")
        except VerifyError as e:
            print(e)
            print("retry...")
            self.jwglLogin(tryNum)      #若登录不成功则递归调用自身

    def getPastGrade(self):
        """
        获取历年成绩
        """
        self.response = self.session.send(self.prepareGetGrade(), timeout=5)
        self.response = self.session.send(self.preparePastGrade(), timeout=5)
        gradeMat = self.formatTable(self.response.text)
        gradeMat = [[row[i] for i in range(len(row)) if i in self.remainList] for row in gradeMat]
        self.outputTable(gradeMat, outputPath='grade.md')

    def getPastSchedule(self, xn_ ,xq_):
        self.response = self.session.send(self.prepareSchedule(), timeout=5)
        self.response = self.session.send(self.preparePastSchedule(xn_, xq_), timeout=5)
        scheduleMat = self.formatTable(self.response.text)
        with open('schedule.md', 'w') as fr:
            fr.write(str(scheduleMat))
        #self.outputTable(scheduleMat, outputPath='schedule.md')

    def getClassList(self):
        self.response = self.session.send(self.prepareClass(), timeout=5)
        self.response = self.session.send(self.prepareGetClass(), timeout=5)

    def outputTable(self, tableMat, outputPath):
        """
        将成绩输出成 md 格式
        """
        tableMat.insert(1, [':------' for i in range(len(tableMat[0]))])
        with open(outputPath, 'w') as fr:
            for row in tableMat:
                fr.write('|')
                for each in row:
                    fr.write(each)
                    fr.write('|')
                fr.write('\n')

    def formatTable(self, tableBody):
        """
        将抓取到的成绩解析成列表
        """
        from bs4 import BeautifulSoup
        import re
        soup = BeautifulSoup(tableBody, 'html.parser')
        return soup.br.table
        tableRow = soup.br.table.find_all('tr')
        tableMat = [i.find_all('td') for i in tableRow]
        return [[each.get_text().strip() for each in row] for row in tableMat]

    def clean(self):
        """
        爬取结束关闭会话
        """
        self.session.close()


class VerifyError(Exception):
    """
    验证码错误类
    """
    def __init__(self, errorInfo):
        Exception.__init__(self)
        self.errorInfo = errorInfo
    def __str__(self):
        return self.errorInfo

def main():
    spider = Spider()
    spider.jwglLogin(tryNum=10)
    spider.getPastSchedule('2014-2015', '2')
    spider.clean()

if __name__ == "__main__":
    main()

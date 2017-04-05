#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from requests import Session, Request, exceptions


class Spider(object):
    def __init__(self):
        self.verifyCodeUrl = "http://jwgl.buct.edu.cn/CheckCode.aspx"
        #self.jwglLoginUrl = "http://jwgl.buct.edu.cn"
        self.jwglLoginUrl = "http://jwgl.buct.edu.cn/default2.aspx"
        self.getGradeUrl = "http://jwgl.buct.edu.cn/xscjcx.aspx"
        self.vpnLoginUrl = "https://vpn.buct.edu.cn/dana-na/auth/url_default/login.cgi"
        self.vpnUrl = "https://vpn.buct.edu.cn/dana-na/auth/url_default/welcome.cgi"
        self.vpnHomeUrl = "https://vpn.buct.edu.cn/dana/home/index.cgi"
        self.studentID = '2013012433'
        self.username = '朱浩南'
        self.jwglPassword = 'zhn1106'
        self.vpnPassword = 'zhiwen.COM'

        self.session = requests.Session()
        self.response = self.session.send(self.prepareJwglFirst(), timeout=5)
        print(self.response.url)

        # 实例化验证码识别器对象，识别验证码
        from classifier import Classifier
        self.classifier = Classifier()
        self.classifier.loadTrainingMat()

    def formatHeaders(self, referer=None):
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
        import re
        return re.findall('<.*name="__VIEWSTATE".*value="(.*)?".*/>', self.response.text)[0]

    def prepareJwglFirst(self):
        headers = self.formatHeaders()
        req = Request('GET', self.jwglLoginUrl, headers=headers)
        return self.session.prepare_request(req)

    def prepareJwglLogin(self):
        """
        准备登录 jwgl 需要的 request
        """
        postdata = {
            '__VIEWSTATE': self.getVIEWSTATE(),
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
        req = Request('POST', self.jwglLoginUrl, headers=headers, data=postdata, cookies=self.session.cookies)
        return self.session.prepare_request(req)

    def prepareGetGrade(self):
        headers = self.formatHeaders(self.response.url)
        params = {
            'xh': self.studentID,
            'xm': self.username,
            'gnmkdm': 'N121605',
        }
        req = Request('GET', self.getGradeUrl, headers=headers, params=params, cookies=self.session.cookies)
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
            '__VIEWSTATE': self.getVIEWSTATE(),
            #'__VIEWSTATEGENERATOR':
            'hidLanguage': '',
            'ddlXN': '',
            'ddlXQ': '',
            'ddl_kcxz': '',
            'btn_zcj': '历年成绩',
        }
        req = Request('POST', self.getGradeUrl, headers=headers, params=params, data=postdata, cookies=self.session.cookies)
        return self.session.prepare_request(req)


    def jwglLogin(self, tryNum=10):
        """
        登录教务网
        """
        import re
        tryNum -= 1
        if tryNum < 0:
            print('\n*** stack overflow! exiting...')
            exit(0)

        codeImg = self.session.get(self.verifyCodeUrl, timeout=5)
        with open('check.gif', 'wb') as fr:
            for chunk in codeImg:
                fr.write(chunk)
        self.verCode = self.classifier.recognizer("check.gif")

        try:
            self.response = self.session.send(self.prepareJwglLogin(), timeout=5)
            if re.search(self.studentID, self.response.url):
                print("login successfully!")
                print(self.response.url)
            else:
                print(self.response.request.url)
                print(self.response.url)
                #print(self.response.text)
                raise VerifyError("Wrong Verification code!")
        except VerifyError as e:
            print(e)
            print("retry...")
            self.jwglLogin(tryNum)

    def getGrade(self):
        self.response = self.session.send(self.prepareGetGrade(), timeout=5)
        self.response = self.session.send(self.preparePastGrade(), timeout=5)
        self.formatGrade(self.response.text)

    def outputGrade(self):
        self.gradeMat.insert(1, [':------' for i in range(len(self.gradeMat[0]))])
        with open('grade.md', 'w') as fr:
            for row in self.gradeMat:
                fr.write('|')
                for each in row:
                    fr.write(each)
                    fr.write('|')
                fr.write('\n')

    def formatGrade(self, gradeBody):
        from bs4 import BeautifulSoup
        import re
        soup = BeautifulSoup(gradeBody, 'html.parser')
        gradeRow = soup.br.table.find_all('tr')
        gradeMat = [i.find_all('td') for i in gradeRow]
        self.gradeMat = [[each.get_text().strip() for each in row] for row in gradeMat]

    def clean(self):
        self.session.close()


class VerifyError(Exception):
    def __init__(self, errorInfo):
        Exception.__init__(self)
        self.errorInfo = errorInfo
    def __str__(self):
        return self.errorInfo

def main():
    spider = Spider()
    spider.jwglLogin(tryNum=10)
    spider.getGrade()
    spider.outputGrade()
    spider.clean()

if __name__ == "__main__":
    main()

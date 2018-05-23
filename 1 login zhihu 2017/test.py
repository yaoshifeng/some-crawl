#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time

# 此处验证码可以在github上调用图像识别，输入图片获取对应验证码
# 目前只支持手动输入...
def captcha(captcha_data):
    with open("captcha.jpg", "wb") as f:
        f.write(captcha_data)
    return input("请输入验证码：")

def zhihuLogin():
    # 构建一个Session对象，保存Cookie
    sess = requests.Session()

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/52.0.2743.116 '
                     'Safari/537.36 '
                     'Edge/15.15063'
    }
    # 首先获取登录页面，找到需要POST的数据(_xsrf)，同时会记录当前网页的Cookie值
    html = sess.get("https://www.zhihu.com/#signin", header = headers).text
    # 调用lxml解析库
    bs = BeautifulSoup(html, "lxml")
    # 获取之前get的页面里的_xsrf值

    # _xsrf作用：防止CSRF攻击(跨站请求伪造)，通常叫做跨域攻击，一种利用网站对用户的一种信任机制来破坏
    # 跨域攻击通常通过伪装成网站信任的用户的请求(利用Cookie)，盗取用户信息，欺骗web服务器
    # 所以网站会通过设置一个隐藏字段来存放这个MD5字符串，这个字符串用来校验用户Cookie和服务器Session一种方式
    _xsrf = bs.find("input", attrs={"name":"_xsrf"}).get("value")

    # 验证码https://www.zhihu.com/captcha.gif?r=1484701999889&type=login
    # r=当前时间戳(从1970年一月一日到现在的秒数)*1000 保留整数

    # 发送验证码图片的请求
    captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login" % (time.time() * 1000)
    captcha_data = sess.get(captcha_url, header=headers).content
    # 获取验证码
    text = captcha(captcha_data)

    data = {
        "_xsrf": _xsrf,
        "email": "yourownemail",
        "password": "yourownpassword",
        "captcha": text,
    }

    response = sess.post("https://www.zhihu.com/login/email", data = data, headers = headers)
    print(response.text)
    #理论上得到“登录成功”的utf-8编码

if __name__ == "__main__":
    zhihuLogin()

















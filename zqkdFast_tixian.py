'''
cron： 0 3 9 * *

new Env('中青看点极速版提现')

变量名：zqkdFastCookie，抓https://user.youth.cn/FastApi/Alipay/withdraw.json（支付宝提现，推荐）
或 https://user.youth.cn/v1/Withdraw/wechat.json（微信提现）

可与leaf共用变量，多了money=0.3，微信要求全部头
'''


#coding=utf-8

import requests
import json
import os
import re

user=os.environ['zqkdFastCookie']
userInfos=user.split('@')
def getScore(userInfo):
    userID=re.findall('(?<=uid=).+?(?=&)',userInfo)
    # money=re.findall('(r"\d+\.?\d*"',userInfo)
    # reg=re.compile(r"(?<=money=)\d+")
    # money=reg.search(userInfo)

    # print(money)
    return
    BASE_URL='https://user.youth.cn/v1/user/userinfo.json'
    headers = {
    "User-Agent":'Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 hap/1.10/xiaomi com.miui.hybrid/1.10.3.3 com.youth.kandianquickapp/2.6.9 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":""}})',
    "Connection":"Keep-Alive",
    "content-type":"application/x-www-form-urlencoded; charset=utf-8",
    "Accept":"application/json",
    "Accept-Encoding":"gzip",
    "Host": "user.youth.cn"
    }
    url=BASE_URL+"?"+userInfo
    try:
        response = requests.get(url, headers=headers)

        response.raise_for_status()

        response.encoding = response.apparent_encoding


        content = response.text
        #print(content)
        data=json.loads(content)
        score=data['items']['score']
        if(int(score)>3000):#默认提现0.3
            print('用户(',userID,')积分(',score,')>3000,执行提现：')
            getMoneyZFB(userInfo) #默认提现到支付宝
            getMoneyWX(userInfo)
    except Exception as e:

        print("请求错误：", e)


##支付宝提现        
def getMoneyZFB(userInfo):
    url = 'https://user.youth.cn/FastApi/Alipay/withdraw.json'
    headers = {
    "User-Agent":'Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 hap/1.10/xiaomi com.miui.hybrid/1.10.3.3 com.youth.kandianquickapp/2.6.9 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":""}})',
    "Connection":"Keep-Alive",
    "content-type":"application/x-www-form-urlencoded; charset=utf-8",
    "Accept":"application/json",
    "Accept-Encoding":"gzip",
    "Host": "user.youth.cn"
     }
    
    try:
        response = requests.post(url,data=userInfo, headers=headers)

        response.raise_for_status()

        response.encoding = response.apparent_encoding


        content = response.text
        #print(content)
        data=json.loads(content)
        print(data['message'])
    except Exception as e:

        print("请求错误：", e)

##微信提现
def getMoneyWX(userInfo):
    url = 'https://user.youth.cn/v1/Withdraw/wechat.json'
    headers = {
    "User-Agent":'Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 hap/1.10/xiaomi com.miui.hybrid/1.10.3.3 com.youth.kandianquickapp/2.6.9 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":""}})',
    "Connection":"Keep-Alive",
    "content-type":"application/x-www-form-urlencoded; charset=utf-8",
    "Accept":"application/json",
    "Accept-Encoding":"gzip",
    "Host": "user.youth.cn"
     }
    
    try:
        response = requests.post(url,data=userInfo, headers=headers)

        response.raise_for_status()

        response.encoding = response.apparent_encoding

        content = response.text
        #print(content)
        data=json.loads(content)
        print(data['message'])
    except Exception as e:

        print("请求错误：", e)

for userInfo in userInfos:
    getScore(userInfo.strip ())

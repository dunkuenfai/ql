'''
cron 30 8 * * *
new Env('中青看点极速版提现')

变量名：zqkdFastCookie，抓https://user.youth.cn/FastApi/Alipay/withdraw.json（支付宝提现，推荐）
或 https://user.youth.cn/v1/Withdraw/wechat.json（微信提现）

可与leaf共用变量，多了money，微信要求全部头
'''


#coding=utf-8

import requests
import json
import os
import re


user=os.environ['zqkdFastCookie']
userInfos=user.split('@')
def getList():
#    import requests
    try:
        url = "https://pms-gateway-web.spaceplat.com/estate/inspection/inspectiontask/page"

        payload = "{\r\n    \"estateType\":1,\r\n    \"countType\":1,\r\n    \"curPage\":1,\r\n    \"pageSize\":50}"
        headers = {
  'Accesstoken': 'Bearer ZH_00009:eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiJ0ZXN0IiwibG9naW5NZXRob2QiOm51bGwsInRlbmVtZW50Q29kZSI6IlpIXzAwMDA5IiwiZXhwIjoxNjkxNDY4Mjk5LCJpYXQiOjE2OTAxNzIyOTksImFjY291bnQiOiIxNTkxNzEwMDIxNyJ9.RtV88Wu5fpizHAvMtCn_kGMqBB4WwIC8aAobCCcJxKA',
  'Authorization': 'Bearer ZH_00009:eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiJ0ZXN0IiwibG9naW5NZXRob2QiOm51bGwsInRlbmVtZW50Q29kZSI6IlpIXzAwMDA5IiwiZXhwIjoxNjkxNDY4Mjk5LCJpYXQiOjE2OTAxNzIyOTksImFjY291bnQiOiIxNTkxNzEwMDIxNyJ9.RtV88Wu5fpizHAvMtCn_kGMqBB4WwIC8aAobCCcJxKA',
  'Content-Type': 'application/json;charset=UTF-8',
  'X-Space-Projectcodes': 'ZH_00009_XM_00000001'
}

        response = requests.request("POST", url, headers=headers, data=payload)

        data=json.loads(response.text)
        # print(data['data'])
        return data['data']
    except Exception as e:
        return []
        print("请求错误：", e)


def hasStr(a,b):
    for c in a:
        if c in b:
            return True
    return False

"""pushplus"""
def pushMsn(token,title,content):

    try:

        url = "http://www.pushplus.plus/send"
        params={
            "token":{token},
            "title":title,
            "content":content,
            "template":"json"
        }

        response = requests.post(url, params =params)

        response.raise_for_status()

        response.encoding = response.apparent_encoding

        data=json.loads(response.text)

        #print(data)
        
    except Exception as e:

        print("push消息错误", e)

def start():
    msg=""
    items=getList()
    arr=["管理","包装","工艺员","设备员"]
    #print(arr)
    
    for item in items:
        if(hasStr(arr,item["planName"])):
            msg=msg+ item['planName']+"\n"
            msg=msg+ ("结束时间："+item['endTime'])+"\n"
            msg=msg+ ("任务状态："+item['taskStatusText'])+"\n"
            msg=msg+ "巡检完成情况："+str(item['doneSubtaskNum'])+'/'+str(item['totalSubtaskNum'])+"\n"
            #print ("doneSubtaskNum",item['doneSubtaskNum'])
            msg=msg+ ("===================================")+"\n"
    print(msg)
    pushMsn('9265ac3f9ab34138a56f68a1c4624e93','巡检提醒',msg)

    # print(data)

if __name__ == '__main__':
    start()


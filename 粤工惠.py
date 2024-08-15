"""
cron: 1 0  0,22 * * *
new Env('粤工惠')

 粤工惠 小程序
 获取'Authorization':"Bearer ****"
 export yghCK='****'
 多账号换行
"""

import requests, json, time, random, os,datetime


ck = ""

import requests
import json
import datetime
def share():

  url = "https://matrix-api.gdftu.org.cn/api/v1/enduser/event/quiz-for-points-v1"

  payload = json.dumps({
  "payload": {
    "action": "start",
    "shared": True
  }
})
  headers = {
  'Host': 'matrix-api.gdftu.org.cn',
  'Connection': 'keep-alive',
  'Content-Length': '44',
  'content-type': 'application/json',
  'Authorization': 'Bearer '+ck,
  'Accept': 'application/json, text/plain, */*',
  'Accept-Encoding': 'gzip,compress,br,deflate',
  'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.50(0x18003237) NetType/WIFI Language/zh_CN',
  'Referer': 'https://servicewechat.com/wxfcc5a91b4f0d6e38/205/page-frame.html'
}

  try:

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    print('分享成功！')
  except Exception as e:
    print(e)


def getTotalSize():
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday
    url = "https://matrix-api.gdftu.org.cn/api/v1/enduser/event/quiz-for-points-v1/result?limit=10&offset=0&startTime="+str(yesterday)+"T16%3A00%3A00.000Z&endTime="+str(today)+"T15%3A59%3A59.999Z&descending=false"
    
    payload = {}
    headers = {
      'Host': 'matrix-api.gdftu.org.cn',
      'Content-Type': 'application/json',
      'Connection': 'keep-alive',
      'Accept': 'application/json, text/plain, */*',
      'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/20) uni-app',
      'Authorization': 'Bearer '+ck,
      'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
      'Accept-Encoding': 'gzip, deflate, br'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    
        a=json.loads(response.text)
        #print(a)
        b=a["totalSize"]
        return(b)
    except Exception as e:
        print('获取答题信息失败，请检查CK')
        return(e)
    
def getQus():

  url = "https://matrix-api.gdftu.org.cn/api/v1/enduser/event/quiz-for-points-v1"

  payload = json.dumps({
  "payload": {
    "action": "start",
    "simulation": False
    }
  })
  headers = {
  'Host': 'matrix-api.gdftu.org.cn',
  'Content-Type': 'application/json',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive',
  'Accept': 'application/json, text/plain, */*',
  'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/20) uni-app',
  'Authorization': 'Bearer '+ck,
  'Content-Length': '49',
  'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
  }
  try:

    response = requests.request("POST", url, headers=headers, data=payload)

    a=json.loads(response.text)
#   print(a)
    b=(a['data']['questionSet'])
    c={
      "payload":{
          "action":"submit",
          "choices":{
              "0":b["0"]["answer"],
              "1":b["1"]["answer"],
              "2":b["2"]["answer"],
              "3":b["3"]["answer"],
              "4":b["4"]["answer"]
          },
          "elapsed": "1.37,2.61,3.77,4.93,5.55",
          "simulation": False
      }
    }
#   print(c)
    return c
  except Exception as e:
        #print(e)
        return(None)  
  
def postAns(answer):
    if(answer==None):
        print('答题错误!已完成答题任务或CK已过期')
        return False

    url = "https://matrix-api.gdftu.org.cn/api/v1/enduser/event/quiz-for-points-v1"
    
    payload = json.dumps(answer)
    headers = {
      'Host': 'matrix-api.gdftu.org.cn',
      'Content-Type': 'application/json',
      'Accept-Encoding': 'gzip, deflate, br',
      'Connection': 'keep-alive',
      'Accept': 'application/json, text/plain, */*',
      'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/20) uni-app',
      'Authorization': 'Bearer '+ck,
      'Content-Length': '143',
      'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    
        print(response.text)
        return True
    except Exception as e:
        print(e)
def creditTasks():
    url = "https://matrix-api.gdftu.org.cn/api/v1/enduser/credit-task"

    payload = {}
    headers = {
        "Host": "matrix-api.gdftu.org.cn",
        "Connection": "keep-alive",
        "Authorization": "Bearer " + ck,
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.44(0x18002c2b) NetType/WIFI Language/zh_CN",
        "Referer": "https://servicewechat.com/wxfcc5a91b4f0d6e38/152/page-frame.html",
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        ret = json.loads(response.text)
        return ret["creditTasks"]
    except Exception as e:
        print(e)


def report(userStatusType):
    url = "https://matrix-api.gdftu.org.cn/api/v1/enduser/user/status-report"

    payload = json.dumps({"userStatusType": userStatusType})
    headers = {
        "Host": "matrix-api.gdftu.org.cn",
        "Connection": "keep-alive",
        "Content-Length": "55",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + ck,
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.44(0x18002c2b) NetType/WIFI Language/zh_CN",
        "Referer": "https://servicewechat.com/wxfcc5a91b4f0d6e38/152/page-frame.html",
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        if "code" in response.text:
            print(json.loads(response.text))
    except Exception as e:
        print(e)


def balance():
    url = "https://matrix-api.gdftu.org.cn/api/v1/enduser/rewards/balance"

    payload = {}
    headers = {
        "Host": "matrix-api.gdftu.org.cn",
        "Connection": "keep-alive",
        "Authorization": "Bearer " + ck,
        "content-type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.44(0x18002c2b) NetType/WIFI Language/zh_CN",
        "Referer": "https://servicewechat.com/wxfcc5a91b4f0d6e38/153/page-frame.html",
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)

        return json.loads(response.text)
    except Exception as e:
        print(e)

def main():
    n=getTotalSize()
    if(type(n)!=int):
        return
    print("今天已答题数：",n)
    if(n<6):
        share()
    # getQus()
    # return
    res=True
    while res:
        res = postAns(getQus())
    tasks = creditTasks()
    for task in tasks:
        requiredCompletionCount = int(task["requiredCompletionCount"])
        completedCount = int(task["completedCount"])
        remainCount = requiredCompletionCount - completedCount
        print("任务：", task["taskType"], "*", remainCount)
        for i in range(remainCount):
            if "USER_CONTINUOUS_SIGN_IN" not in task["taskType"]:
                userStatusType = "USER_STATUS_TYPE_" + task["taskType"][12:]
                report(userStatusType)
                t = random.uniform(0, 2)
                print(i + 1)
                time.sleep(t)
    jifen = balance()["balance"]
    print("任务完成，当前积分：", jifen)
    print("==========================================================")


if __name__ == "__main__":
    yghCKs = os.environ["yghCK"].split()
    print("共找到", len(yghCKs), "个账号")
    i = 0
    for yghCK in yghCKs:
        i = i + 1
        ck = yghCK
        print("开始第", i, "个账号")
        main()

"""
cron: 0 0  7,23 * * *
new Env('安学网')

配置文件增加
export client_id='***'
export client_secret='***'

环境变量access_token，name#access_token，多变量换行

by dunkuenfai

"""



import requests
import json
from Crypto.Hash import SHA256
from Crypto.Hash import MD5
import string
import random
from datetime import datetime
import os

client_id=os.environ['client_id']
client_secret=os.environ['client_secret']
ql_url='http://localhost:5700'

refresh_token_list=[]
access_token = ""
refresh_token=""

ql_Token=''

def getCode(phone):
    TIMESTAMP = getTimeStamp()
    # print(TIMESTAMP)
    var2 = "";
    NONCE = getRandomString(11);
    var2 = createSign(TIMESTAMP, TIMESTAMP);
    texts = "NONCE=" + NONCE + "&SIGN=" + var2 + " & SIGN_TYPE = SHA256&TIMESTAMP = " + TIMESTAMP
    texts=texts.replace(" ","")

    url = 'https://safetyinformation.cn/api/admin/mobile/autoRegLoginMsg/' + phone + '?' + texts
    print(url)
    payload = {}
    headers = {
  'Host': 'safetyinformation.cn',
  'Cookie': 'JSESSIONID=sXaxifeju5AnrQLI3WyNTqBCQ_UL0Jfmt1uSvrbl',
  'Connection': 'keep-alive',
  'API-VERSION': '2',
  'Accept': '*/*',
  'User-Agent': 'AnXueWang/3.0.5 (iPad; iOS 15.4.1; Scale/2.00)',
  'Accept-Language': 'zh-Hans-US;q=1, en-US;q=0.9',
  'Authorization': 'Basic aW9zOmlvcw==',
  'Accept-Encoding': 'gzip, deflate, br'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def getCk(phone, code):
    url = "https://safetyinformation.cn/api/auth/app/token/sms?app=APPSMS@" + phone + "&code=" + code;

    headers = {
    "Host": "safetyinformation.cn",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "API-VERSION": "2",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9",
    "Authorization": "Basic aW9zOmlvcw==",
  }
    data=setData()['jsons']

    response = requests.request("POST", url, headers=headers, data=data)

    print(response.text)


'''
签到
'''
def  postSign():
    headers = {
    "Host": "safetyinformation.cn",
    "Connection": "keep-alive",
    "API-VERSION": "2",
    "Accept": "*/*",
    "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9",
    "Authorization": "Bearer " + access_token,
    "Accept-Encoding": "gzip, deflate, br"
  }
    url = "https://safetyinformation.cn/api/share/usersign/sign";
    urlData = setData()['jsons'];
    response = requests.request("POST", url, headers=headers, data=urlData)
    res=json.loads(response.text)
    # print(res)
    if(res['code']==0):
        print('签到任务成功！')
    else:
        print('签到任务失败：',res['msg'])

'''
每日分享
'''
def  postShare():
    headers = {
    "Host": "safetyinformation.cn",
    "Connection": "keep-alive",
    "API-VERSION": "2",
    "Accept": "*/*",
    "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9",
    "Authorization": "Bearer " + access_token,
    "Accept-Encoding": "gzip, deflate, br"
  }
    url = "https://safetyinformation.cn/api/share/userpointstask/completeByType/article_share";
    urlData = setData()['jsons']
    response = requests.request("POST", url, headers=headers, data=urlData)
    res=json.loads(response.text)
    if(res['code']==0):
        print('分享任务成功！')
    else:
        print('分享任务失败！请检查网络参数')

'''
获取挑战答题题目 并提交
'''
def getTZquestions():
    header = {
    "Host": "safetyinformation.cn",
    "Connection": "keep-alive",
    "API-VERSION": "2",
    "Accept": "*/*",
    "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9",
    "Authorization": "Bearer " + access_token,
    "Accept-Encoding": "gzip, deflate, br"
    }
    url = "https://safetyinformation.cn/api/share/challengeExam/start?" + setData()['texts'];
    response = requests.request("GET", url, headers=header)
    res=json.loads(response.text)
    # print(res)
    Tid=res['data']['id']
    postTZ(Tid)

'''
挑战答题提交
'''
def postTZ(Tid):
    urlData = setData()['jsons'];
    url = "https://safetyinformation.cn/api/share/challengeExam/end"
    rightQuestionNum=random.randint(10,100)
    payload = json.dumps({
  "TIMESTAMP": urlData['TIMESTAMP'],
  "SIGN":  urlData['SIGN'],
  "rightQuestionNum": rightQuestionNum,
  "SIGN_TYPE": "SHA256",
  "chaId": Tid,
  "NONCE": urlData['NONCE'],
    })
    headers = {
  'Host': 'safetyinformation.cn',
  'Content-Type': 'application/json',
  'Accept-Encoding': 'gzip, deflate, br',
  'API-VERSION': '2',
  'Connection': 'keep-alive',
  'Accept': '*/*',
  'User-Agent': 'AnXueWang/3.0.5 (iPad; iOS 15.4.1; Scale/2.00)',
  'Accept-Language': 'zh-Hans-US;q=1, en-US;q=0.9',
  'Authorization': 'Bearer '+ access_token,
  'Content-Length': '211'
}

    response = requests.request("POST", url, headers=headers, data=payload)
    res=json.loads(response.text)
    if(res['code']==0):
        print("挑战答题成功，共答对" + str(rightQuestionNum) + "题")
    else:
        print('挑战答题错误，请检查网络参数')
  

'''
每日答题
'''
def  postDailyquestions():
    url = "https://safetyinformation.cn/api/share/user/exam/v2/daily/submit"
    urlData = setData()['jsons']
    payload = json.dumps({
  "ques": [{
        "userAnswer": [
          "25115378829905"
        ],
        "id": 7705051592210,
        "originOptions": [
          25111994955351,
          25113228547212,
          25115378829905,
          25117650216784
        ]
      },
      {
        "userAnswer": [
          "25182434257475"
        ],
        "id": 7720633838107,
        "originOptions": [
          25176244434964,
          25179180766231,
          25181038477630,
          25182434257475
        ]
      },
      {
        "userAnswer": [
          "25307161599435"
        ],
        "id": 7754553526450,
        "originOptions": [
          25301025856917,
          25303710167472,
          25304283416881,
          25307161599435
        ]
      },
      {
        "userAnswer": [
          "25331027055198"
        ],
        "id": 7759820648701,
        "originOptions": [
          25325932342573,
          25328271786387,
          25331027055198,
          25331745946710
        ]
      },
      {
        "userAnswer": [
          "25342878062834"
        ],
        "id": 7763764455771,
        "originOptions": [
          25342878062834,
          25345369944059,
          25348422072409,
          25350875937996
        ]
      },
      {
        "userAnswer": [
          "25405096193460"
        ],
        "id": 7780838278601,
        "originOptions": [
          25402820878062,
          25405096193460
        ]
      },
      {
        "userAnswer": [
          "25424909495182"
        ],
        "id": 7791339313953,
        "originOptions": [
          25424909495182,
          25426814344148
        ]
      },
      {
        "userAnswer": [
          "27800202918282",
          "27802247437557",
          "27804515683883",
          "27807720024795"
        ],
        "id": 8450910815495,
        "originOptions": [
          27800202918282,
          27802247437557,
          27804515683883,
          27807720024795,
          27808447960056
        ]
      },
      {
        "userAnswer": [
          "27876999047668",
          "27879117867807",
          "27882876657246",
          "27884362568310"
        ],
        "id": 8471118324680,
        "originOptions": [
          27876999047668,
          27879117867807,
          27882876657246,
          27884362568310
        ]
      },
      {
        "userAnswer": [
          "35723101403237",
          "35723688481134",
          "35725828565740"
        ],
        "id": 8476098472467,
        "originOptions": [
          35723101403237,
          35723688481134,
          35725828565740,
          35728185771510
        ]
      }
    ],
  "subType": 2,
    "SIGN_TYPE": "SHA256",
    "TIMESTAMP": urlData['TIMESTAMP'],
    "useTimeSeconds": random.randint(10,100),
    "SIGN": urlData['SIGN'],
    "startTime": datetime.now().strftime('%Y-%m-%-d %H:%M:%S'),
    "NONCE": urlData['NONCE']
})
    headers = {
  'Host': 'safetyinformation.cn',
  'Content-Type': 'application/json',
  'Accept-Encoding': 'gzip, deflate, br',
  'API-VERSION': '2',
  'Connection': 'keep-alive',
  'Accept': '*/*',
  'User-Agent': 'AnXueWang/3.0.5 (iPad; iOS 15.4.1; Scale/2.00)',
  'Accept-Language': 'zh-Hans-US;q=1, en-US;q=0.9',
  'Authorization': 'Bearer '+access_token,
  'Content-Length': '1566'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    ret=json.loads(response.text)
    if(ret['code']==0):
        print("每日答题结果:每日答题完成")
    else:
        print("每日答题错误：" + ret['msg'])

'''
根据refresh_token获取token
'''
def getToken(refresh_token):
    url = "https://safetyinformation.cn/api/auth/oauth/token?refresh_token="+refresh_token+"&grant_type=refresh_token&scope=server"

    payload = json.dumps({
  "grant_type": "refresh_token",
  "scope": "server",
  "refresh_token":refresh_token
    })
    headers = {
  'Host': 'safetyinformation.cn',
  'Content-Type': 'application/json',
  'Accept-Encoding': 'gzip, deflate, br',
  'API-VERSION': '2',
  'Connection': 'keep-alive',
  'Accept': '*/*',
  'User-Agent': 'AnXueWang/3.0.5 (iPad; iOS 15.4.1; Scale/2.00)',
  'Accept-Language': 'zh-Hans-US;q=1, en-US;q=0.9',
  'Authorization': 'Basic aW9zOmlvcw==',
  'Content-Length': '102'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    ret=json.loads(response.text)
    
    return ret
    
def getToken2(refresh_token):
    import requests

    url = "https://safetyinformation.cn/api/auth/oauth/token?grant_type=refresh_token&scope=server&refresh_token="+refresh_token

    payload = {}
    headers = {
  'authority': 'safetyinformation.cn',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'zh-CN,zh;q=0.9',
  'authorization': 'Basic c2hhcmU6c2hhcmU=',
  'content-length': '0',
  'content-type': 'application/x-www-form-urlencoded',
  'cookie': 'JSESSIONID=PJD_kY4iyr7sDNUI9YXPN-FCc14ZW8MyzY0a1f07',
  'origin': 'https://safetyinformation.cn',
  'referer': 'https://safetyinformation.cn/safety',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15 Edg/119.0.0.0'
}


    response = requests.request("POST", url, headers=headers, data=payload)
    ret=json.loads(response.text)
    
    return ret

'''
生成url字符及挑战答题json
'''
def setData():
    TIMESTAMP = getTimeStamp()
    var2 = "";
    NONCE = getRandomString(11);
    var2 = createSign(NONCE, TIMESTAMP);
    texts = "&NONCE=" + NONCE + "&SIGN=" + var2 + " & SIGN_TYPE = SHA256&TIMESTAMP = " + TIMESTAMP

    jsons = {
    "NONCE": NONCE,
    "TIMESTAMP": TIMESTAMP,
    "SIGN_TYPE": "SHA256",
    "bankIds": ["41", "42"],
    'SIGN':var2,
    'startTime':TIMESTAMP
  }
    ret={}
    ret['texts']=texts
    ret['jsons']=jsons
    return ret
'''
生成sign字符
'''
def createSign(NONCE, TIMESTAMP):
    ret = ""
    data = NONCE + TIMESTAMP
    ret = data
    md5=MD5.new(ret.encode(encoding='UTF-8')).hexdigest()
    ret = "TIMESTAMP=" + TIMESTAMP + "&NONCE=" + NONCE + "&SIGN_TYPE=SHA256&SECRET_KEY=" + md5
    h = SHA256.new(ret.encode(encoding='UTF-8')).hexdigest()
    return h.upper()



'''
格式化时间
'''
def getTimeStamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')

'''
获取随机字符串
'''
def getRandomString(L):
    return"".join(random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(L))




'''
青龙面板API
'''

def getUser():
    url = ql_url+"/open/auth/token?client_id="+client_id+"&client_secret="+client_secret
    payload = {}
    headers = {
  'accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    ret=json.loads(response.text)
    return(ret['data']['token'])

def getEvns():

    url = ql_url+"/open/envs"

    payload = {}
    headers = {

  'accept': 'application/json',
  'Content-Type': 'application/json;charset=UTF-8',
  'Authorization':'Bearer '+ql_Token
}

    response = requests.request("GET", url, headers=headers, data=payload)
    ret=json.loads(response.text)
    datas=ret['data']
    re_data=''
    for data in datas:
        if(data['name']=='anxue_token'):
            envId=data['id']
            re_data = data
            # print(data['value'])
    # print(envId)
    return re_data

def updateEvn(id,value):
    url = ql_url+"/open/envs"

    payload = json.dumps({
    "value": value,
    "name": "anxue_token",
    "remarks": "安学网refreshtoKen",
    "id": id
    })
    headers = {
  'accept': 'application/json',
  'Authorization': 'Bearer '+ql_Token,
  'Content-Type': 'application/json'
}

    response = requests.request("PUT", url, headers=headers, data=payload)
    ret=json.loads(response.text)
    if(ret['code']==200):
        print('环境变量更新成功！')
    else:
        print('环境变量更新失败！')


def main():
    refresh_token_tmp=''
    global  ql_Token,access_token
    ql_Token=getUser()
    envs=getEvns()
    refresh_token_list=envs['value'].split()
    refresh_list=[]#更新后的数组
    for refresh_token_tmp in refresh_token_list:
        a=refresh_token_tmp.split('#')
        refresh_token=a[len(a)-1]
        refresh=getToken2(refresh_token)
        # print(refresh)
        if ('code' not in refresh):
            b=refresh['name']+'#'+refresh['refresh_token']
            refresh_list.append(b)
            # print(refresh)
            access_token=refresh['access_token']
            print('🎈🎈',b,'🎈🎈')
            postSign()# 每日签到
            postShare()#每日分享
            postDailyquestions()#m每日答题
            getTZquestions() #挑战答题
            getTZquestions() #挑战答题
        else:
            refresh_list.append('已过期#'+refresh_token)


    value=0
    if(len(refresh_list)>0):
        value=''
    for s in refresh_list:
        value=value+s+'\n'
    updateEvn(envs['id'],value.strip())

if __name__ == "__main__":
     main()
    


     

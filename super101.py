"""
cron: 1 0  0 * * *
new Env('super101签到')
参数自行修改
"""
import requests, json,os
from sendNotify import send


token = os.environ["super101"]


#坐标：
payload = json.dumps({
  "Longitude": 110.95701600000007,
  "Latitude": 21.654112000000016
})
headers = {
  'Host': 'capi.jingjianx.vip',
  'Authorization': 'Bearer '+token,
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090b19)XWEB/11275',
  'Bdszh-Shopid': '13586',
  'Content-Type': 'application/json',
  'Xweb_xhr': '1',
  'Jj-Shopid': '13586',
  'Jj-Miniappversion': '10.14.9t',
  'Jj-Chainid': '3091',
  'Jj-Appid': 'wx0aab473f5689b342',
  'Accept': '*/*',
  'Sec-Fetch-Site': 'cross-site',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://servicewechat.com/wx0aab473f5689b342/14/page-frame.html',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Connection': 'close'}
try:
    url = "https://capi.jingjianx.vip/signed/capp/signed/confirm"
    response = requests.post(url=url, headers=headers, data=payload)
    print(response.text)
except Exception as e:
    msg="签到失败："+ e
    send("super101",mssg)
try:
    url="https://capi.jingjianx.vip/signed/capp/signed/getprogress"

    response=requests.get(url=url, headers=headers)
    signinday=(json.loads(response.text)['data']['signInDays'])
    msg='已连续签到：'+str(signinday)+'天。'
    print(msg)
    send("super101",msg)
except Exception as e:
    msg="签到失败："+ e
    print(msg)

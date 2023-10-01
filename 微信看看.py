import requests
import time
import json
import re


ysmuid='29a3867bb367ca26196405d8ebcea04d'
uk=''
unionid='oZdBp05So3-mR3-0TQwJgvAo3iGw'

def getUk():

  url = "http://1695977764.szcoin.site/yunonline/v1/wtmpdomain"

  payload = "unionid="+unionid
  headers = {
  'Host': '1695977764.szcoin.site',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'X-Requested-With': 'XMLHttpRequest',
  'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
  'Accept-Encoding': 'gzip, deflate',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': 'http://1695977764.szcoin.site',
  'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42(0x18002a28) NetType/WIFI Language/zh_CN',
  'Connection': 'keep-alive',
  'Referer': 'http://1695977764.szcoin.site/?cate=0',
  'Content-Length': '36',
  'Cookie': 'ejectCode=1; ysmuid=29a3867bb367ca26196405d8ebcea04d'
}

  response = requests.request("POST", url, headers=headers, data=payload)

  data=json.loads(response.text)
  link=(data['data']['domain'])
  n=link.find('uk')
  link=link[n+3:n+35]
  global uk
  uk=link


def remain():

  url = "http://1696031853.szcoin.site/yunonline/v1/gold?unionid="+unionid

  payload = {}
  headers = {
  'Host': '1696031853.szcoin.site',
  'Accept-Encoding': 'gzip, deflate',
  'Cookie': 'ejectCode=1; ysmuid='+ysmuid,
  'Connection': 'keep-alive',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42(0x18002a28) NetType/WIFI Language/zh_CN',
  'Referer': 'http://1696031853.szcoin.site/?cate=0',
  'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
  'X-Requested-With': 'XMLHttpRequest'
}

  response = requests.request("GET", url, headers=headers, data=payload)

  data=json.loads(response.text)
  remains=int(data['data']['remain_read'])
  return(remains)


def step1():
  url = "http://1696006141.tyjnwb.top/?cate=0"

  payload = {}
  headers = {
  'Host': '1696006141.tyjnwb.top',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Cookie': 'ysmuid='+ysmuid,
  'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42(0x18002a28) NetType/WIFI Language/zh_CN',
  'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}

  response = requests.request("GET", url, headers=headers, data=payload)


def step2():

  url = "https://nsr.zsf2023e458.cloud/yunonline/v1/do_read?uk="+uk

  payload = {}
  headers = {
  'Host': 'nsr.zsf2023e458.cloud',
  'Origin': 'https://d1695975741-1258867400.cos.ap-beijing.myqcloud.com',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42(0x18002a28) NetType/WIFI Language/zh_CN',
  'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}

  response = requests.request("GET", url, headers=headers, data=payload)

  data=response.text
  link = re.search('link ', data, re.M | re.I)
  
  print(link)

def step3():

  url = "http://1695976419.szcoin.site/yunonline/v1/jump?key=eyJpdiI6IkRsc3dBcTBOUng1NWpHOEdKSDh4a2c9PSIsInZhbHVlIjoibDVRUTRxSmVSbzNhcERYa3AwbDVPYWtadVllME41aW9uTzQxaW1zYnhuUUVLSUdHaHp5WU9OSXQrcmlIQk5CNWdIRitGeFZcL0FzMlNQajJoK3RITDc3a0I0bE5IN0lrN01tNExONURtYXRuVldMXC9MSGhDMHZjcTI0Z1Qxazdzd0NEd0tjUXRWKys2V3ZGelwvK1JBdU82MldmZmppb1k5a2FVK1NRU3VXZG96bGY2MDZ5eGoxU1VHakY0QTlyanZEIiwibWFjIjoiMmU4Nzk5MjhkMWRhNWViNjQ1OGViNDVmZDdmNjE4NzM1YzZlZWY0NjNlOGQ2MGMwNzQxMjcyMTFhNzQ2MjFhYSJ9&state=1&unionid=oZdBp05So3-mR3-0TQwJgvAo3iGw?/"

  payload = {}
  headers = {
  'Host': '1695976419.szcoin.site',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Upgrade-Insecure-Requests': '1',
  'Cookie': 'ysmuid='+ysmuid,
  'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42(0x18002a28) NetType/WIFI Language/zh_CN',
  'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
  'Accept-Encoding': 'gzip, deflate',
  'Connection': 'keep-alive'
}

  response = requests.request("GET", url, headers=headers, data=payload)

  #print(response.text,1)


def step4():

  url = "https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?time=30&timestamp=1695976911000&uk="+uk

  payload = {}
  headers = {
  'Host': 'nsr.zsf2023e458.cloud',
  'Origin': 'https://d1695975741-1258867400.cos.ap-beijing.myqcloud.com',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42(0x18002a28) NetType/WIFI Language/zh_CN',
  'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}

  response = requests.request("GET", url, headers=headers, data=payload)
  data=json.loads(response.text)
  print(data)

def main():    
  step1()
  time.sleep(3)
  step2()
  time.sleep(3)
  step3()
  time.sleep(3)
  step4()

if __name__=="__main__":
  remain()
  getUk()
  #step2()
  for a in range(0,3):
    main()
    



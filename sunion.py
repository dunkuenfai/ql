'''
cron: 0 0 21 * * *
new Env('正能量')
'''
import requests
import time
import json
import os 
from datetime import date,datetime
from datetime import timedelta
#https://weapp.zhdy.es668.cn/records?access-token=hJMVgtfhfmBJrlrzV-efVM2HiGonH5OA

token=os.environ['znl']
# 签到
msg=""
params = {"records":[
            {"value":"按时起床,一日之际在于晨","type":"10"},
            {"value":"做好早餐给小孩","type":"10"},
            {"value":"早上送女儿上学","type":"10"},
            {"value":"做好防疫措施","type":"10"},
            {"value":"上班路上礼让行人","type":"10"},
            {"value":"路上顺利顺路接同事","type":"10"},
            {"value":"坚持8点前到岗","type":"10"},
            {"value":"到公司见到同事打招呼","type":"10"},
            {"value":"打开办公室窗户通风","type":"10"},
            {"value":"为办公室煮开水","type":"10"},
            {"value":"交接班聆听安全之歌，弘扬正能量事","type":"10"},
            {"value":"交接班合理安排当天工作，提醒同事注意作业安全","type":"10"},
            {"value":"交完班帮忙收拾凳子","type":"10"},
            {"value":"按时对装置进行巡检","type":"10"},
            {"value":"办公尽量使用电子版，减少纸张，节约一分钱","type":"10"},
            {"value":"保持台面清洁","type":"10"},
            {"value":"中午午休期间尽量不发出声响以免影响同事休息","type":"10"},
            {"value":"节约水资源，不浪费一滴水","type":"10"},
            {"value":"不浪费一度电，及时关闭没有在用电器","type":"10"},
            {"value":"宣传众和正能量故事","type":"10"},
            {"value":"感恩众和","type":"10"},
            {"value":"坚持每天学习","type":"10"},
            {"value":"坚持写正能量","type":"10"},
            {"value":"坚持写工作日志","type":"10"},
            {"value":"下班路上礼让行人","type":"10"},
            {"value":"辅导儿子做作业","type":"10"},
            {"value":"检查女儿英语作业情况","type":"10"},
            {"value":"吃完饭收拾碗筷并洗碗","type":"10"},
            {"value":"陪父母聊天","type":"10"},
            {"value":"晚上在家坚持锻炼身体","type":"10"},
            {"value":"鼓励小孩坚持锻炼身体","type":"10"},
            {"value":"调好水温给小孩洗澡","type":"10"},
            {"value":"将换下来的脏衣服拿到洗衣机洗","type":"10"},
            {"value":"提醒小孩到点睡觉，早睡早起","type":"10"},
            {"value":"听新闻热点，快速了解国内外大事","type":"10"},
            {"value":"关注天气预报，了解天气情况","type":"10"},
            {"value":"做明天的工作计划","type":"10"},
            {"value":"微笑面对所有困难，给自己打气","type":"10"},
            ]}
# params={"records":[{"value":"做好备件计划","type":"10"}]}

def zhengnengliang():

    try:

        url = "https://weapp.zhdy.es668.cn/records?access-token="+token
        headers = {
    "host":"weapp.zhdy.es668.cn",
    "Connection":"keep-alive",
    "content-type":"application/json",
    "Accept":"application/json",
    "Accept-Encoding":"gzip,compress,br,deflate",
    "User-Agent":"Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d2f) NetType/WIFI Language/zh_CN",
    "Referer":"https://servicewechat.com/wx22189b1374bef585/17/page-frame.html"

     }

        # print(params)
        
        # 发送一个请求

        response = requests.post(url, json=params, headers=headers)

        response.raise_for_status()

        response.encoding = response.apparent_encoding

        # 由于返回的是JSONP数据，所以不能用response.json()来解析

        content = response.text
        #print(content)
        data=json.loads(content)
        print(data,'\n共发布 ',len(params),' 条正能量' )

        # 截取JSONP中的JSON数据
        return

        data = json.loads(content[content.find("{"):content.rfind(")")])

        if data.get("error_code") == 0:

            print("发布成功：", data.get("data").get("checkin_num"))

        else:

            print("发布失败，原因：", data.get("error_msg"))

    except Exception as e:

        print("发布错误；", e)


def paiming():
    now=datetime.now()
    today = now.strftime("%Y-%m-%d")
    month =now.strftime("%Y-%m-")+"1"
    # print(month)
    global  msg
    try:
       url = "https://weapp.zhdy.es668.cn/paimings/latest/1?access-token=" +token
       headers={
        "host":"weapp.zhdy.es668.cn",
        "Connection":"keep-alive",
        "content-type":"application/json",
        "Accept":"application/json",
        "Accept-Encoding":"gzip,compress,br,deflate",
        "User-Agent":"Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d2f) NetType/WIFI Language/zh_CN",
        "Referer":"https://servicewechat.com/wx22189b1374bef585/17/page-frame.html"
       }
       data={
           "today":0,
           "date":[month,today],
           "sort":"total_record",
           "keyword":"苏杰万"
       }
       response = requests.post(url, json=data, headers=headers)
       response.raise_for_status()
       response.encoding = response.apparent_encoding
       content = response.text
       data=json.loads(content)["data"]["set"][0]
       paihang=data["ranking"]
       children=data["children"]
       msg=msg+("小组排名"+str(paihang)+"名\n")
       for item in children:
           msg=msg+(item["name"]+" "+str(item["total"])+"条\n")
       msg=msg+"\n"

    except Exception as e:
        print("查询错误；", e)



def toutiao():

    try:

        url = "https://www.toutiao.com/api/pc/feed/"

        headers = {
    "Connection":"keep-alive",
    "content-type":"application/json",
    "accept-encoding":"gzip, deflate, br",
    "Accept-Encoding":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36 Edg/110.0.1587.63"

      }

        

        # 发送一个请求

        response = requests.get(url,headers=headers)

        response.raise_for_status()
        data = response.json()['data']

        if len(data)<5:
            print('获取列表小于5条，结束！！！')
            return
        for i in range(5):
            content={}
            value=data[i]['title']
            content['value']="阅读新闻《"+value+"》"
            content['type']=10
            params['records'].append(content)
        #print(list)
        #params['records'].append(list[0])

        
    except Exception as e:

        print("读取头条失败", e)




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




def main():
    global msg
    #print("-------------------获取头条列表-------------------")

    toutiao()
    #print("-------------------获取头条结算-------------------")

    #print("-------------------发布开始-------------------")

    zhengnengliang()
    # pushMsn('9265ac3f9ab34138a56f68a1c4624e93','龙虎榜','111')
    paiming()

    #print("-------------------发布结束-------------------")
    msg=msg+str(params)
    pushMsn('9265ac3f9ab34138a56f68a1c4624e93','正能量',msg)
    print(msg)


if __name__ == "__main__":

    main()

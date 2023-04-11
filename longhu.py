'''
cron: 0 0 20 * * *
new Env('龙虎榜')
'''
import requests
import time
import json
import datetime
from chinese_calendar import is_workday, is_holiday
from datetime import date,datetime
from datetime import timedelta
headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Referer": "https://emdata.eastmoney.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  }
msg=''
 


def is_work_day():
    """判断是否工作日"""
    now = datetime.now()
    # today = now.strftime("%Y%m%d") #获取到"20210111"这个字符串
    # nowatime = now.strftime("%H:%M:%S") #获取到"20:05:51"这个字符串
    # today = now.strftime("%Y,%m,%d") #获取到"2021-01-11"这个字符串
    april_last = date(2023, 3,19)   # datetime.date
    # april_last = datetime.now().strftime("%Y%m%d")
    print(is_workday(now))     # True
    print(is_holiday(april_last))     # False
    print(april_last.weekday())       # 5-星期六
    # print(str(today))
    lastday=get_pervious_work_day(now)
    print(lastday)
 
 
def get_pervious_work_day(day: datetime):
    """获取上一个工作日"""
    day = day - timedelta(days=1)
    if is_workday(day):
        return day
    return get_pervious_work_day(day)

def longhu():
    print('获取龙虎榜。。。。。。。。。。')
    global msg
    try:
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        lastday=get_pervious_work_day(now).strftime("%Y-%m-%d")
        url = "https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_ORGANIZATION_TRADE_DETAILSNEW&sty=ALL&source=DataCenter&client=WAP&p=1&ps=20&sr=-1&st=RATIO&filter=(TRADE_DATE%3E=%27"+lastday+"%27)(TRADE_DATE%3C=%27"+today+"%27)"


        # 发送一个请求

        response = requests.get(url,headers)

        response.raise_for_status()
        success=response.json()['success']
        if(success==False):
            print('返回数据为空')
            return
        # print(response.text)
        data = response.json()['result']['data']
        msg=msg+('-------------------------------------------\n')
        msg=msg+('          龙虎榜机构买入超5%：\n')
        msg=msg+('-------------------------------------------\n')
        msg=msg+('名   称 '+'代   码 '+'当天升幅 '+'买入占比\n')
        
        for i in data:
            if(i['RATIO']>5):
                msg=msg+(i['SECURITY_NAME_ABBR']+" "+i["SECURITY_CODE"]+" "+str(round(i['CHANGE_RATE'],2))+'%'+" "+str(round(i['RATIO'],2))+'%\n')
        msg=msg+('-------------------------------------------'+'\n')
        
    except Exception as e:

         msg=msg+("读取龙虎榜失败"+e)

def get_organization():
    '''获取机构3天上涨排行'''
    print('获取机构3天上涨排行。。。。。。。。。。')
    global msg
    msg=msg+('-------------------------------------------\n')
    msg=msg+('机构买入3天上涨排行近期交易数据\n')
    msg=msg+('-------------------------------------------\n')
    # msg.join ('机构买入3天上涨排行近期交易数据')
    try:
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        lastday=get_pervious_work_day(now).strftime("%Y-%m-%d")
        url = "https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_OPERATEDEPT_RETURN_RANKING&sty=ALL&source=DataCenter&client=WAP&p=1&ps=300&sr=-1&st=AVERAGE_INCREASE_2DAY&filter=(STATISTICSCYCLE=%2203%22)&?v=02695676277618384"
        
        # 发送一个请求

        response = requests.get(url,headers)

        response.raise_for_status()
        success=response.json()['success']
        # print(response.json())
        if(success==False):
            msg=msg+('返回数据为空\n')
            return
        # print(response.text)
        data = response.json()['result']['data']
        # print(data[0]['TOTAL_BUYER_SALESTIMES_1DAY'])
        # return
        # get_org_buy(data[0]['OPERATEDEPT_CODE'])
        # return
        for item in data:
            # print(item['TOTAL_BUYER_SALESTIMES_1DAY'])
            if(type(item['TOTAL_BUYER_SALESTIMES_1DAY'])==int and item['TOTAL_BUYER_SALESTIMES_1DAY']>5):
                    
                if(get_org_buy(item['OPERATEDEPT_CODE'])):
                    
                    msg=msg+('      '+item['OPERATEDEPT_CODE']+" "+
                    str(item['TOTAL_BUYER_SALESTIMES_1DAY'])+" "+
                    str(round(item['AVERAGE_INCREASE_3DAY'],2))+'%'+" "+
                    item['OPERATEDEPT_NAME']+"\n"
                    )
                    msg=msg+('==================================================\n')



        

    except Exception as e:

        print("读取龙虎榜失败", e)    


def get_org_buy(code):
    '''获取机构近5天交易'''
    global msg
    url='https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_OPERATEDEPT_TRADE_DETAILSNEW&sty=SECURITY_CODE,SECURITY_NAME_ABBR,TRADE_DATE,OPERATEDEPT_NAME,ACT_BUY,ACT_SELL,NET_AMT,EXPLANATION,D1_CLOSE_ADJCHRATE,D2_CLOSE_ADJCHRATE,D3_CLOSE_ADJCHRATE,D5_CLOSE_ADJCHRATE,D10_CLOSE_ADJCHRATE,D20_CLOSE_ADJCHRATE,D30_CLOSE_ADJCHRATE,SECUCODE&p=1&ps=20&st=TRADE_DATE&sr=-1&filter=(OPERATEDEPT_CODE%3D%22'+code+'%22)&?v=018168881062146247'
    response = requests.get(url,headers)
    response.raise_for_status()
    success=response.json()['success']
    # print(response.json())
    if(success==False):
        msg=msg+('返回数据为空\n')
        return
    data = response.json()['result']['data']
    for item in data:
        # print(item['TRADE_DATE'])
        time1 = time.mktime(time.strptime(item['TRADE_DATE'], '%Y-%m-%d %H:%M:%S'))
        nowTime =  time.mktime(time.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d'))
        # print(item['NET_AMT']>0)
        if((nowTime - time1)<5*24*60*60 and item['NET_AMT']>0):
            msg=msg+(item['SECURITY_CODE']+" "+item['SECURITY_NAME_ABBR']+" "+item['TRADE_DATE']+" "+str(item['NET_AMT'])+"\n")
            return True
    return False
    # print(data)

"""pushplus"""
def pushMsn(token,title,content):

    try:

        url = "http://www.pushplus.plus/send"
        params={
            "token":{token},
            "title":title,
            "content":content,
            "data":[]
            # "template":"json"
        }

        response = requests.post(url, params =params)

        response.raise_for_status()

        response.encoding = response.apparent_encoding

        data=json.loads(response.text)

        print(data)
        
    except Exception as e:

        print("push消息错误", e)

def main():
    global msg
    msg=msg+'###########################################\n'
    get_organization()
    msg=msg+'###########################################\n'
    longhu()
    pushMsn('9265ac3f9ab34138a56f68a1c4624e93','龙虎榜',msg)
    print(msg)
if __name__ == "__main__":

    main()

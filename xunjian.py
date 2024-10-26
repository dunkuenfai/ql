'''
cron 0 0 12,4,5 * * *
new Env('巡检提醒')

公司内部应用
'''


#coding=utf-8

import requests
import json
import os
import re
from sendNotify import send

cookie=os.environ['xunjianCookie']
def getList():
#    import requests
    try:
        url = "https://pms-gateway-web.spaceplat.com/estate/inspection/inspectiontask/page"

        payload = "{\r\n    \"estateType\":1,\r\n    \"countType\":1,\r\n    \"curPage\":1,\r\n    \"pageSize\":50}"
        headers = {
  'Accesstoken': 'Bearer '+cookie,
  'Authorization': 'Bearer '+cookie,
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



def start():
    msg=""
    items=getList()
    arr=["管理","包装","工艺员","设备员","综合"]
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
    send('巡检提醒',msg)

    # print(data)

if __name__ == '__main__':
    start()


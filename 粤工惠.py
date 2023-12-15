"""
cron: 0 0  8,22 * * *
new Env('粤工惠')

 粤工惠 小程序
 获取'Authorization':"Bearer ****"
 export yghCK='****'
 多账号换行
"""

import requests, json, time, random, os


ck = ""


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

    response = requests.request("GET", url, headers=headers, data=payload)
    ret = json.loads(response.text)
    return ret["creditTasks"]


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

    response = requests.request("POST", url, headers=headers, data=payload)

    if "code" in response.text:
        print(json.loads(response.text))


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

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


def main():
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

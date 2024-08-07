"""
cron: 0 0 0,17 * * *
new Env('应急普法')


export YJPF='Authorizationlg'


by dunkuenfai

"""

import requests
import json
import random
import os
from random import randint

TiMu = [
    "cd45229d28e1464aa2b8ecfd6b134f40#B",
    "019d75797d94426581f54351d8337d5c#C",
    "54c087dca289442ea906022825fff158#A",
    "d3e07a6cd79943739beeb5691bd588fd#C",
    "edc6b59c4c2b44dfb38c110dde52a6ab#B",
    "326e236c299f4bcd82a3a9fe1914e5f7#B",
]


def getUserData(token):

    url = "https://yjpf.mem.gov.cn/app/emdguard/userdata/emdGuard2024"

    payload = {}
    headers = {
        "Host": "yjpf.mem.gov.cn",
        "Accept": "application/json, text/plain, */*",
        "Uuid": "6500329083",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090b13) XWEB/11065 Flue",
        "Authorizationlg": "Bearer " + token,
        "Origin": "https://yjpfjt.mem.gov.cn",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://yjpfjt.mem.gov.cn/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close",
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    if data["code"] == 200:
        print(
            "账号:",
            data["data"]["simple"]["nickName"],
            "  积分:",
            data["data"]["score"]["sumScore"],
        )


def PostAnswer(token):
    answer = random.sample(TiMu, 5)
    times = 0
    answerStr = ""
    for i in range(len(answer)):
        time = randint(1000, 5000)
        answer[i] = answer[i] + "#" + str(time) + "##"
        times = times + time
        answerStr = answerStr + answer[i]
    answerStr = '"{\\"answer\\":\\"' + answerStr + \
        '\\",\\"time\\":' + str(times) + "}"
    payload = (
        '{"projectId":"emdGuard2024","dtId":"emd_guard2024_exam","json":'
        + answerStr
        + '"}'
    )

    url = "https://yjpf.mem.gov.cn/app/emdguard/dt/saveEmdGuardExamUserAnswer"

    headers = {
        "Host": "yjpf.mem.gov.cn",
        "uuid": "6500329083",
        "Accept": "application/json, text/plain, */*",
        "AuthorizationLg": "Bearer " + token,
        "Sec-Fetch-Site": "same-site",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Mode": "cors",
        "Content-Type": "application/json;charset=utf-8",
        "Origin": "https://yjpfjt.mem.gov.cn",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.50(0x18003236) NetType/WIFI Language/zh_CN",
        "Referer": "https://yjpfjt.mem.gov.cn/",
        "Content-Length": "309",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
    }
    # return
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)
        if data["code"] == 2002:
            print("今日答题完成")
            return 2002
        if data["code"] == 200:
            print("答对题数：", data["data"]["answer"]["rightTi"])
            return 200
        return 0
    except Exception as e:
        print(e)


def main(ck):

    code = 0
    while code != 2002:
        code = PostAnswer(ck)
    getUserData(ck)


if __name__ == "__main__":
    cks = os.environ["YJPF"].split()
    for ck in cks:
        main(ck)

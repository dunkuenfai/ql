
'''
cron: 0 0  7 * * *
new Env('星空穿透签到')

随便写，不确定能用

把账号密码写到19，20行

by dunkuenfai

'''



import requests
from sendNotify import send

username = ""
password = ""


base_url = "https://frp.starryfrp.com/console/"


def login2():
    url = "https://frp.starryfrp.com/auth/login/login?r_u=http%3A%2F%2Ffrp.starryfrp.com%2Fconsole%3F"

    payload = "username=" + username + "&password=" + password
    headers = {
        "Host": "frp.starryfrp.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://frp.starryfrp.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": "PHPSESSID=mmrgqii03jb1j453knfka8aue3",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/115.0.1901.203 Version/15.0 Mobile/15E148 Safari/604.1",
        "Referer": "https://frp.starryfrp.com/auth/login/?r_u=http%3A%2F%2Ffrp.starryfrp.com%2Fconsole%3F",
        "Content-Length": "37",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        print(response)
    except Exception as e:
        print("请求错误：", e)
        send("星空内网穿透签到", e)





def doSign():
    headers = {
        "Cookie": "Hm_lvt_b0484d537cf505eb114b28a53d0859b1=1691801331,1691987527; Hm_lpvt_b0484d537cf505eb114b28a53d0859b1=1691987533; PHPSESSID=mmrgqii03jb1j453knfka8aue3"
    }
    csrf_token = "06bef213cfa84366ee91bd1cd1889478"
    url = base_url + "Signc/Sign?csrf=" + csrf_token
    payload = {}
    try:
        rsp = requests.request("GET", url, headers=headers, data=payload)
        print(rsp.text)
        send("星空内网穿透签到", rsp.text)
    except Exception as e:
        print("请求错误：", e)
        send("星空内网穿透签到", e)


if __name__ == "__main__":
    login2()
    doSign()

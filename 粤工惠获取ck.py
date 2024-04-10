'''
用来快速获取粤工惠CK,非青龙脚本，请安装python后运行。
by dunkuenfai
2024.04.10

'''

import requests
import json


def getMSN(phone):
    url = (
        "https://matrix-api.gdftu.org.cn/api/v1/enduser/otp?phone.areaCode=86&otpType=OTP_TYPE_LOGIN&phone.nationalNumber="
        + phone
    )

    payload = {}
    headers = {
        "Host": "matrix-api.gdftu.org.cn",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/20) uni-app",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        print("请稍后，正在获取验证码。。。")
    except Exception as e:
        print(e)


def getCK(phone, code):
    url = "https://matrix-api.gdftu.org.cn/api/v1/enduser/login"

    payload = json.dumps(
        {
            "loginType": "LOGIN_TYPE_SMS_OTP",
            "smsOtpLoginInput": {
                "phone": {"areaCode": "86", "nationalNumber": phone},
                "code": code,
            },
        }
    )
    headers = {
        "Host": "matrix-api.gdftu.org.cn",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/20) uni-app",
        "Content-Length": "128",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)
        print("已获得CK：", data["token"])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    phone = input("请输入手机号码，按回车确定： ")
    getMSN(phone)
    code = input("请输入验证码，按回车确定： ")
    getCK(phone, code)

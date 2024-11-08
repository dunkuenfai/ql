"""
cron: 1 0  2,22 * * *
new Env('ikuu机场签到')

"""

import requests, json, re, os
from sendNotify import send
session = requests.session()
# 配置用户名（一般是邮箱）
email = os.environ.get('EMAIL')
# 配置用户名对应的密码 和上面的email对应上
passwd = os.environ.get('PASSWD')

base_url = 'https://ikuuu.top' #这个网址可能会变，按实际修改

login_url = base_url + '/auth/login'
check_url = base_url + '/user/checkin'
info_url = base_url + '/user/profile'

header = {
        'origin': 'https://ikuuu.pw',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
data = {
        'email': email,
        'passwd': passwd
}
try:
    print('进行登录...')
    response = json.loads(session.post(url=login_url,headers=header,data=data).text)
    print(response['msg'])
    # 获取账号名称
    info_html = session.get(url=info_url,headers=header).text
    # 进行签到
    result = json.loads(session.post(url=check_url,headers=header).text)
    print(result['msg'])
    content = result['msg']
    send("ikuu签到",content)
    print('推送成功')
except:
    content = '签到失败'
    send("ikuu签到",content)

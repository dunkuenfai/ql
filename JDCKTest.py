'''
cron: 0 0 * * * *
new Env('京东CK检测备注')
须更新下面三个参数
ddress = "*****"
client_id = "*****"
client_secret = "*****"
检测是否过期并禁用/启用，没有备注的以用户名为备注
'''
import re
import json
import os
import requests
from json import dumps as jsonDumps
address = "http://127.0.0.1:5800"
client_id = "_HX3HJfzOV3G"
client_secret = "Lrie2fsj-_NnDYD88h56w5sg"


class QL:
    auth = ""

    def __init__(self, address: str, id: str, secret: str) -> None:
        """
        初始化
        """
        self.address = address
        self.id = id
        self.secret = secret
        self.valid = True
        self.login()

    def log(self, content: str) -> None:
        """
        日志
        """
        print(content)

    def login(self) -> None:
        """
        登录
        """
        url = f"{self.address}/open/auth/token?client_id={self.id}&client_secret={self.secret}"
        try:
            rjson = requests.get(url).json()
            if (rjson['code'] == 200):
                self.auth = f"{rjson['data']['token_type']} {rjson['data']['token']}"
            else:
                self.log(f"登录失败：{rjson['message']}")
        except Exception as e:
            self.valid = False
            self.log(f"登录失败：{str(e)}")

    def getEnvs(self) -> list:
        """
        获取环境变量
        """
        url = f"{self.address}/open/envs?searchValue="
        headers = {"Authorization": self.auth}
        try:
            rjson = requests.get(url, headers=headers).json()
            if (rjson['code'] == 200):
                return rjson['data']
            else:
                self.log(f"获取环境变量失败：{rjson['message']}")
        except Exception as e:
            self.log(f"获取环境变量失败：{str(e)}")

    def deleteEnvs(self, ids: list) -> bool:
        """
        删除环境变量
        """
        url = f"{self.address}/open/envs"
        headers = {"Authorization": self.auth,
                   "content-type": "application/json"}
        try:
            rjson = requests.delete(
                url, headers=headers, data=jsonDumps(ids)).json()
            if (rjson['code'] == 200):
                self.log(f"删除环境变量成功：{len(ids)}")
                return True
            else:
                self.log(f"删除环境变量失败：{rjson['message']}")
                return False
        except Exception as e:
            self.log(f"删除环境变量失败：{str(e)}")
            return False

    def addEnvs(self, envs: list) -> bool:
        """
        新建环境变量
        """
        url = f"{self.address}/open/envs"
        headers = {"Authorization": self.auth,
                   "content-type": "application/json"}
        try:
            rjson = requests.post(url, headers=headers,
                                  data=jsonDumps(envs)).json()
            if (rjson['code'] == 200):
                self.log(f"新建环境变量成功：{len(envs)}")
                return True
            else:
                self.log(f"新建环境变量失败：{rjson['message']}")
                return False
        except Exception as e:
            self.log(f"新建环境变量失败：{str(e)}")
            return False

    def updateEnv(self, env: dict) -> bool:
        """
        更新环境变量
        {
            name,
            value,
            remarks,
            _id}
        """
        url = f"{self.address}/open/envs"
        headers = {"Authorization": self.auth,
                   "content-type": "application/json"}
        try:
            rjson = requests.put(url, headers=headers,
                                 data=jsonDumps(env)).json()
            if (rjson['code'] == 200):
                # self.log(f"更新环境变量成功")
                return True
            else:
                # self.log(f"更新环境变量失败：{rjson['message']}")
                return False
        except Exception as e:
            # self.log(f"更新环境变量失败：{str(e)}")
            return False

    def enable(self, id_list):
        """
        启用环境变量

        :param id_list: 环境变量ID列表
        :return: 响应结果json
        """
        url = f"{self.address}/open/envs/enable"
        headers = {"Authorization": self.auth,
                   "content-type": "application/json"}
        data = json.dumps(id_list)
        res = requests.put(url=url, headers=headers, data=data).json()
        return res

    def disable(self, id_list):
        """
        禁用环境变量

        :param id_list: 环境变量ID列表
        :return: 响应结果json
        """
        url = f"{self.address}/open/envs/disable"
        headers = {"Authorization": self.auth,
                   "content-type": "application/json"}
        data = json.dumps(id_list)
        res = requests.put(url=url, headers=headers, data=data).json()
        return res


def getJDcK(envs):
    data = []
    for env in envs:
        if env["name"] == "JD_COOKIE":
            data.append(env)
    return data


def getUserInfo(env):
    ck = env["value"]
    # print(ck)

    url = 'https://api.m.jd.com/api?functionId=getUserAllPinInfo&appid=jd-cphdeveloper-m&body=%7B%22tenantCode%22%3A%22jgm%22%2C%22bizModelCode%22%3A%226%22%2C%22bizModeClientType%22%3A%22M%22%2C%22externalLoginType%22%3A%221%22%2C%22url%22%3A%22https%3A%2F%2Fmy.m.jd.com%2Faccount%2Findex.html%3Fsceneval%3D2%26jxsid%3D17524716738817430777%26appCode%3Dms0ca95114%26source%3Dcommon%26urlHiddenHeader%3Dfalse%22%2C%22sid%22%3A%22%22%2C%22USER_FLAG_CHECK%22%3A%22%22%7D&loginType=2&sceneval=2&g_login_type=1&g_ty=ajax&appCode=ms0ca95114'

    headers = {
        'Cookie': ck,
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        'Accept': "application/json",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-gpc': "1",
        'sec-ch-ua-platform': "\"Windows\"",
        'sec-ch-ua': "\"Not?A_Brand\";v=\"99\", \"Chromium\";v=\"130\"",
        'dnt': "1",
        'sec-ch-ua-mobile': "?0",
        'origin': "https://my.m.jd.com",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://my.m.jd.com/",
        'accept-language': "zh-CN,zh;q=0.9",
        'priority': "u=1, i",
    }
    try:
        requests.packages.urllib3.disable_warnings()
        resp = requests.get(url=url, verify=False,
                            headers=headers, timeout=60).json()
        if (resp["errcode"] == 0) :
            remark = resp["userdata"]["renderJdData"][0]["msg"]["nickName"]
            
            env['enable']=True
            if (env["remarks"] == ""):
                env["remarks"] = remark

        else:
            env['enable']=False

    except Exception as e:
        print(e)
    return (env)


if __name__ == "__main__":

    ql = QL(address, client_id, client_secret)
    envs = ql.getEnvs()
    datas = getJDcK(envs)
    # print(datas[0])
    # updatamsg = getUserInfo(datas[0])
    # ql.updateEnv({
    #             "id": updatamsg["id"],
    #             "name": updatamsg["name"],
    #             "value": updatamsg["value"],
    #             "remarks": updatamsg["remarks"]
    #         })
    for data in datas:
        updatamsg = getUserInfo(data)
        # print(updatamsg)
        # ql.updateEnv(updatamsg)
        # print(updatamsg)
        if (updatamsg["enable"]):
            ql.updateEnv({
                "id": updatamsg["id"],
                "name": updatamsg["name"],
                "value": updatamsg["value"],
                "remarks": updatamsg["remarks"]
            })
            print(f"{updatamsg['remarks']} 已启用")
        else:
            print(f"{updatamsg['remarks']} 已禁止")

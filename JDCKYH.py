'''
cron: 0 0 * * * *
new Env('京东CK优化')
须更新下面三个参数

'''
import re
import requests
from json import dumps as jsonDumps
address = "http://127.0.0.1:5700"
client_id = "286cRep426R_"
client_secret = "_hNEoPHu6OWmqk217bfW7qQc"


class QL:
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
        """
        url = f"{self.address}/open/envs"
        headers = {"Authorization": self.auth,
                   "content-type": "application/json"}
        try:
            rjson = requests.put(url, headers=headers,
                                 data=jsonDumps(env)).json()
            if (rjson['code'] == 200):
                self.log(f"更新环境变量成功")
                return True
            else:
                self.log(f"更新环境变量失败：{rjson['message']}")
                return False
        except Exception as e:
            self.log(f"更新环境变量失败：{str(e)}")
            return False


def updataJDcK(envs):
    data = []
    for env in envs:
        if env["name"] == "JD_COOKIE":
            ck = env["value"]
            a = re.findall(r"(pt_key=.+?pt_pin=.+?;)", ck)
            if (len(a) == 1):
                # print(a[0])
                env["value"] = a[0]
                data.append(env)
    return (data)


if __name__ == "__main__":

    ql = QL(address, client_id, client_secret)

    envs = ql.getEnvs()
    datas = updataJDcK(envs)
    for data in datas:
        print(data["value"], ql.updateEnv({
            "id": data["id"],
            "name": data["name"],
            "value": data["value"],
            "remarks": data["remarks"]
        }))

#!/usr/bin/python3
'''
cron: 0 0 9/21 * * *
new Env('i茅台')
脚本参考：https://github.com/gerenyongcangku/imaotai
'''

import logging
import sys

import datetime
import json
import math
import random
import re
import time
import requests
import hashlib
import logging
import pytz
from Crypto.Cipher import AES
import base64
import os

configs = os.environ["Imaotai"]
configs=a=eval(configs)
#格式如下：抓包取得token，lat和lng代表经纬度，可在https://lbs.amap.com/tools/picker获得
#  [{
#     'phone': '159********',
#     'province': '广东省',
#     'city': '**市',
#     'token': '***',
#     'userid': '11672*****',
#     'lat': '***.56797',
#     'lng': '***.90431'
# }]


print(configs)

class Encrypt:
    def __init__(self, key, iv):
        self.key = key.encode('utf-8')
        self.iv = iv.encode('utf-8')

    # @staticmethod
    def pkcs7padding(self, text):
        """明文使用PKCS7填充 """
        bs = 16
        length = len(text)
        bytes_length = len(text.encode('utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding
        self.coding = chr(padding)
        return text + padding_text

    def aes_encrypt(self, content):
        """ AES加密 """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        # 处理明文
        content_padding = self.pkcs7padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result

    def aes_decrypt(self, content):
        """AES解密 """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        content = base64.b64decode(content)
        text = cipher.decrypt(content).decode('utf-8')
        return text.rstrip(self.coding)


# process.py
AES_KEY = 'qbhajinldepmucsonaaaccgypwuvcjaa'
AES_IV = '2018534749963515'
SALT = '2af72f100c356273d46284f6fd1dfc08'


current_time = str(int(time.time() * 1000))
headers = {}
mt_version = "".join(re.findall('latest__version">(.*?)</p>',
                                requests.get(
                                    'https://apps.apple.com/cn/app/i%E8%8C%85%E5%8F%B0/id1600482450').text,
                                re.S)).split(" ")[1]

header_context = f'''
MT-Lat: 28.499562
MT-K: 1675213490331
MT-Lng: 102.182324
Host: app.moutai519.com.cn
MT-User-Tag: 0
Accept: */*
MT-Network-Type: WIFI
MT-Token: 1
MT-Team-ID: 
MT-Info: 028e7f96f6369cafe1d105579c5b9377
MT-Device-ID: 2F2075D0-B66C-4287-A903-DBFF6358342A
MT-Bundle-ID: com.moutai.mall
Accept-Language: en-CN;q=1, zh-Hans-CN;q=0.9
MT-Request-ID: 167560018873318465
MT-APP-Version: 1.3.7
User-Agent: iOS;16.3;Apple;?unrecognized?
MT-R: clips_OlU6TmFRag5rCXwbNAQ/Tz1SKlN8THcecBp/HGhHdw==
Content-Length: 93
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Type: application/json
userId: 2
'''


def init_headers(user_id: str = '1', token: str = '2', lat: str = '28.499562', lng: str = '102.182324'):
    for k in header_context.rstrip().lstrip().split("\n"):
        temp_l = k.split(': ')
        dict.update(headers, {temp_l[0]: temp_l[1]})
    dict.update(headers, {"userId": user_id})
    dict.update(headers, {"MT-Token": token})
    dict.update(headers, {"MT-Lat": lat})
    dict.update(headers, {"MT-Lng": lng})
    dict.update(headers, {"MT-APP-Version": mt_version})


def signature(data: dict):
    keys = sorted(data.keys())
    temp_v = ''
    for item in keys:
        temp_v += data[item]
    text = SALT + temp_v + current_time
    hl = hashlib.md5()
    hl.update(text.encode(encoding='utf8'))
    md5 = hl.hexdigest()
    return md5


def get_vcode(mobile: str):
    params = {'mobile': mobile}
    md5 = signature(params)
    dict.update(
        params, {'md5': md5, "timestamp": current_time, 'MT-APP-Version': mt_version})
    responses = requests.post("https://app.moutai519.com.cn/xhr/front/user/register/vcode", json=params,
                              headers=headers)

    logging.info(
        f'get v_code : params : {params}, response code : {responses.status_code}, response body : {responses.text}')


def login(mobile: str, v_code: str):
    params = {'mobile': mobile, 'vCode': v_code, 'ydToken': '', 'ydLogId': ''}
    md5 = signature(params)
    dict.update(
        params, {'md5': md5, "timestamp": current_time, 'MT-APP-Version': mt_version})
    responses = requests.post("https://app.moutai519.com.cn/xhr/front/user/register/login", json=params,
                              headers=headers)
    if responses.status_code != 200:
        logging.info(
            f'login : params : {params}, response code : {responses.status_code}, response body : {responses.text}')
    dict.update(headers, {'MT-Token': responses.json()['data']['token']})
    dict.update(headers, {'userId': responses.json()['data']['userId']})
    return responses.json()['data']['token'], responses.json()['data']['userId']


def get_current_session_id():
    day_time = get_day_time()
    responses = requests.get(
        f"https://static.moutai519.com.cn/mt-backend/xhr/front/mall/index/session/get/{day_time}")
    if responses.status_code != 200:
        logging.warning(
            f'get_current_session_id : params : {day_time}, response code : {responses.status_code}, response body : {responses.text}')
    current_session_id = responses.json()['data']['sessionId']
    dict.update(headers, {'current_session_id': str(current_session_id)})


def get_day_time():

    # 创建一个东八区（北京时间）的时区对象
    beijing_tz = pytz.timezone('Asia/Shanghai')

    # 获取当前北京时间的日期和时间对象
    beijing_dt = datetime.datetime.now(beijing_tz)

    # 设置时间为0点
    beijing_dt = beijing_dt.replace(hour=0, minute=0, second=0, microsecond=0)

    # 获取时间戳（以秒为单位）
    timestamp = int(beijing_dt.timestamp()) * 1000
    return timestamp


def get_location_count(province: str,
                       city: str,
                       item_code: str,
                       p_c_map: dict,
                       source_data: dict,
                       lat: str = '28.499562',
                       lng: str = '102.182324'):
    day_time = get_day_time()
    session_id = headers['current_session_id']
    responses = requests.get(
        f"https://static.moutai519.com.cn/mt-backend/xhr/front/mall/shop/list/slim/v3/{session_id}/{province}/{item_code}/{day_time}")
    if responses.status_code != 200:
        logging.warning(
            f'get_location_count : params : {day_time}, response code : {responses.status_code}, response body : {responses.text}')
    shops = responses.json()['data']['shops']

    if MAX_ENABLED:
        return max_shop(city, item_code, p_c_map, province, shops)
    if DISTANCE_ENABLED:
        return distance_shop(city, item_code, p_c_map, province, shops, source_data, lat, lng)


def distance_shop(city,
                  item_code,
                  p_c_map,
                  province,
                  shops,
                  source_data,
                  lat: str = '28.499562',
                  lng: str = '102.182324'):
    # shop_ids = p_c_map[province][city]
    temp_list = []
    for shop in shops:
        shopId = shop['shopId']
        items = shop['items']
        item_ids = [i['itemId'] for i in items]
        # if shopId not in shop_ids:
        #     continue
        if str(item_code) not in item_ids:
            continue
        shop_info = source_data.get(shopId)
        # d = geodesic((lat, lng), (shop_info['lat'], shop_info['lng'])).km
        d = math.sqrt(
            (float(lat) - shop_info['lat']) ** 2 + (float(lng) - shop_info['lng']) ** 2)
        # print(f"距离：{d}")
        temp_list.append((d, shopId))

    # sorted(a,key=lambda x:x[0])
    temp_list = sorted(temp_list, key=lambda x: x[0])
    # logging.info(f"所有门店距离:{temp_list}")
    if len(temp_list) > 0:
        return temp_list[0][1]
    else:
        return '0'


def max_shop(city, item_code, p_c_map, province, shops):
    max_count = 0
    max_shop_id = '0'
    shop_ids = p_c_map[province][city]
    for shop in shops:
        shopId = shop['shopId']
        items = shop['items']

        if shopId not in shop_ids:
            continue
        for item in items:
            if item['itemId'] != str(item_code):
                continue
            if item['inventory'] > max_count:
                max_count = item['inventory']
                max_shop_id = shopId
    logging.debug(
        f'item code {item_code}, max shop id : {max_shop_id}, max count : {max_count}')
    return max_shop_id


encrypt = Encrypt(key=AES_KEY, iv=AES_IV)


def act_params(shop_id: str, item_id: str):

    session_id = headers['current_session_id']
    userId = headers['userId']
    params = {"itemInfoList": [{"count": 1, "itemId": item_id}],
              "sessionId": int(session_id),
              "userId": userId,
              "shopId": shop_id
              }
    s = json.dumps(params)
    act = encrypt.aes_encrypt(s)
    params.update({"actParam": act})
    return params


def send_email(msg: str):
    if PUSH_TOKEN is None:
        return
    title = 'imoutai预约失败'  # 改成你要的标题内容
    content = msg  # 改成你要的正文内容
    url = 'http://www.pushplus.plus/send'
    r = requests.get(url, params={'token': PUSH_TOKEN,
                                  'title': title,
                                  'content': content})
    logging.info(f'通知推送结果：{r.status_code, r.text}')


def reservation(params: dict, mobile: str):
    params.pop('userId')
    responses = requests.post("https://app.moutai519.com.cn/xhr/front/mall/reservation/add", json=params,
                              headers=headers)
    if responses.status_code == 401:
        send_email(f'[{mobile}],登录token失效，需要重新登录')
        raise RuntimeError
    if '您的实名信息未完善或未通过认证' in responses.text:
        send_email(f'[{mobile}],{responses.text}')
        raise RuntimeError
    logging.info(
        f'预约 : mobile:{mobile} :  response code : {responses.status_code}, response body : {responses.text}')


def select_geo(i: str):
    # https://www.piliang.tech/geocoding-amap
    url = f"https://www.piliang.tech/api/amap/geocode?address={i}"
    resp = requests.get(url)
    print(url)
    geocodes: list = resp.json()['geocodes']
    return geocodes


def get_map(lat: str = '28.499562', lng: str = '102.182324'):
    p_c_map = {}
    url = 'https://static.moutai519.com.cn/mt-backend/xhr/front/mall/resource/get'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_1 like Mac OS X)',
        'Referer': 'https://h5.moutai519.com.cn/gux/game/main?appConfig=2_1_2',
        'Client-User-Agent': 'iOS;16.0.1;Apple;iPhone 14 ProMax',
        'MT-R': 'clips_OlU6TmFRag5rCXwbNAQ/Tz1SKlN8THcecBp/HGhHdw==',
        'Origin': 'https://h5.moutai519.com.cn',
        'MT-APP-Version': mt_version,
        'MT-Request-ID': f'{int(time.time() * 1000)}{random.randint(1111111, 999999999)}{int(time.time() * 1000)}',
        'Accept-Language': 'zh-CN,zh-Hans;q=1',
        'MT-Device-ID': f'{int(time.time() * 1000)}{random.randint(1111111, 999999999)}{int(time.time() * 1000)}',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'mt-lng': f'{lng}',
        'mt-lat': f'{lat}'
    }
    res = requests.get(url, headers=headers, )
    mtshops = res.json().get('data', {}).get('mtshops_pc', {})
    urls = mtshops.get('url')
    r = requests.get(urls)
    for k, v in dict(r.json()).items():
        provinceName = v.get('provinceName')
        cityName = v.get('cityName')
        if not p_c_map.get(provinceName):
            p_c_map[provinceName] = {}
        if not p_c_map[provinceName].get(cityName, None):
            p_c_map[provinceName][cityName] = [k]
        else:
            p_c_map[provinceName][cityName].append(k)

    return p_c_map, dict(r.json())


def getUserEnergyAward(mobile: str):
    """
    领取耐力
    """
    cookies = {
        'MT-Device-ID-Wap': headers['MT-Device-ID'],
        'MT-Token-Wap': headers['MT-Token'],
        'YX_SUPPORT_WEBP': '1',
    }
    response = requests.post('https://h5.moutai519.com.cn/game/isolationPage/getUserEnergyAward', cookies=cookies,
                             headers=headers, json={})
    # response.json().get('message') if '无法领取奖励' in response.text else "领取奖励成功"
    logging.info(
        f'领取耐力 : mobile:{mobile} :  response code : {response.status_code}, response body : {response.text}')


########################
# config
ITEM_MAP = {
    "10941": "53%vol 500ml贵州茅台酒（甲辰龙年）",
    "10942": "53%vol 375ml×2贵州茅台酒（甲辰龙年）",
    "10056": "53%vol 500ml茅台1935",
    "2478": "53%vol 500ml贵州茅台酒（珍品）"
}

# 需要预约的商品(默认只预约2个兔茅)
########################
ITEM_CODES = ['10941', '10942']

# push plus 微信推送,具体使用参考  https://www.pushplus.plus
# 例如： PUSH_TOKEN = '123456'
########################
# 不填不推送消息，一对一发送
PUSH_TOKEN = '9265ac3f9ab34138a56f68a1c4624e93'
########################

# credentials 路径，例如：CREDENTIALS_PATH = /home/user/.imoutai/credentials
# 不配置，使用默认路径，在宿主目录
# 例如： CREDENTIALS_PATH = '/home/user/.imautai/credentials'
########################
CREDENTIALS_PATH = None
########################

# 预约规则配置
########################
# 预约本市出货量最大的门店
MAX_ENABLED = True
# 预约你的位置附近门店
DISTANCE_ENABLED = False
########################



DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO,
                    # 定义输出log的格式
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                    stream=sys.stdout,
                    datefmt=DATE_FORMAT)

# 获取当日session id
get_current_session_id()

if len(configs) == 0:
    logging.error("配置文件未找到配置")
    sys.exit(1)

for config in configs:
    mobile = config["phone"]
    province = config['province']
    city = config['city']
    token = config['token']
    userId = config['userid']
    lat = config['lat']
    lng = config['lng']

    p_c_map, source_data = get_map(lat=lat, lng=lng)

    init_headers(user_id=userId, token=token, lng=lng, lat=lat)
    # 根据配置中，要预约的商品ID，城市 进行自动预约
    try:
        for item in ITEM_CODES:
            max_shop_id = get_location_count(province=province,
                                             city=city,
                                             item_code=item,
                                             p_c_map=p_c_map,
                                             source_data=source_data,
                                             lat=lat,
                                             lng=lng)
            print(f'max shop id : {max_shop_id}')
            if max_shop_id == '0':
                continue
            shop_info = source_data.get(str(max_shop_id))
            title = ITEM_MAP.get(item)
            logging.info(f'商品：{title}, 门店：{shop_info["name"]}')
            reservation_params = act_params(max_shop_id, item)
            reservation(reservation_params, mobile)
            getUserEnergyAward(mobile)
    except BaseException as e:
        print(e)
        logging.error(e)

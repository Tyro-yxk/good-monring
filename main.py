from zhdate import ZhDate
from datetime import date, datetime
import math
from wechatpy import WeChatClient, WeChatClientException
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
citys = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ids = os.environ["USER_ID"].split(";")
template_id = os.environ["TEMPLATE_ID"]

he_key = os.environ["HE_KEY"]


# def get_weather(city):
#     url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#     res = requests.get(url).json()
#     weather = res['data']['list'][0]
#     return weather


def get_weather(city, he_key):
    city_url = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(city, he_key)
    city_res = requests.get(city_url).json()
    if city_res["code"] != "200":
        return None
    wea_city = city_res["location"][0]
    cityId = wea_city["id"]
    url = "https://devapi.qweather.com/v7/weather/now?location={}&key={}".format(cityId, he_key)
    res = requests.get(url).json()
    if res["code"] != "200":
        print("天气获取失败")
    else:
        wea = res["now"]

    url = "https://devapi.qweather.com/v7/weather/3d?location={}&key={}".format(cityId, he_key)
    res = requests.get(url).json()
    if res["code"] != "200":
        print("温度最值获取失败")
    else:
        max_temp = res["daily"][0]["tempMax"] + u"\N{DEGREE SIGN}" + "C"
        min_temp = res["daily"][0]["tempMin"] + u"\N{DEGREE SIGN}" + "C"

    # 获取空气质量
    url = "https://devapi.qweather.com/v7/air/now?location={}&key={}".format(cityId, he_key)
    res = requests.get(url).json()
    if res["code"] != "200":
        print("空气质量获取失败")
    else:
        category = res["now"]["category"]
        # pm2.5
        pm2p5 = res["now"]["pm2p5"]
    id = random.randint(1, 16)
    url = "https://devapi.qweather.com/v7/indices/1d?location={}&key={}&type={}".format(cityId, he_key, id)
    res = requests.get(url).json()
    proposal = ""
    if res["code"] != "200":
        print("建议获取失败")
    else:
        proposal += res["daily"][0]["text"]

    weather = {
        "weather": wea["text"],
        "temp": wea["temp"] + u"\N{DEGREE SIGN}" + "C",
        "wind": wea["windDir"],
        "humidity": wea["humidity"],
        "airQuality": category,
        "high": max_temp,
        "low": min_temp,
        "p2m5": pm2p5,
        "province": wea_city["adm1"],  # 省
        "city": wea_city["adm2"]
    }

    return weather


def get_count(start_date):
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday(birthday):
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def weekday():
    week = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return week[date.today().weekday()]


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def split_city():  # 循环列表，多个地址
    if citys is None:
        return None
    return citys.split(";")


def split_birthday():  # 多个生日纪念日
    if birthday is None:
        return None
    return birthday.split(';')


def split_start():  # 多个倒计时通知
    if start_date is None:
        return None
    return start_date.split(";")


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

data = {}
weather = {}
for index, aim_city in enumerate(split_city()):
    ci_name = "city"
    if index != 0:
        ci_name = ci_name + "_%d" % index
    weather = get_weather(aim_city, he_key)
    province = weather["province"]  # 省
    city = weather["city"]  # 市，县，州
    t = aim_city

    if province != city and city != aim_city:
        t = province + "-" + city + "-" + t
    elif city != aim_city:
        t = city + "-" + t
    elif aim_city != province:
        t = province + "-" + t

    data[ci_name] = {
        "value": t,
        "color": get_random_color()
    }
    da = {
        "hu_%s" % ci_name: {  # 空气湿度
            "value": weather["humidity"],
            "color": get_random_color()
        },
        "wi_%s" % ci_name: {  # 风向
            "value": weather["wind"],
            "color": get_random_color()
        },
        "ai_%s" % ci_name: {  # 空气质量
            "value": weather["airQuality"],
            "color": get_random_color()
        },
        "we_%s" % ci_name: {  # 天气
            "value": weather["weather"],
            "color": get_random_color()
        },
        "te_%s" % ci_name: {  # 当前温度
            "value": math.floor(weather['temp']),
            "color": get_random_color()
        },
        "hi_%s" % ci_name: {  # 最高温度
            "value": math.floor(weather['high']),
            "color": get_random_color()
        },
        "lo_%s" % ci_name: {  # 最低温度
            "value": math.floor(weather['low']),
            "color": get_random_color()
        },
        "pm_%s" % ci_name: {
            "value": math.floor(weather["p2m5"]),
            "color": get_random_color()
        }
    }
    data.update(da)
for index, aim_date in enumerate(split_birthday()):
    key_name = "rec"
    if index != 0:
        key_name = key_name + "_%d" % index
    data[key_name] = {
        "value": get_birthday(aim_date),
        "color": get_random_color()
    }

for index, aim_start in enumerate(split_start()):
    key_name = "start"
    if index != 0:
        key_name = key_name + "_%d" % index
    data[key_name] = {  # 多个倒计时纪念
        "value": get_count(aim_start),
        "color": get_random_color()
    }

da = {
    "y_date": {  # 日期，阳历
        "value": today.strftime("%Y年%m月%d日"),
        "color": get_random_color()
    },
    "x_date": {  # 农历日期
        "value": str(ZhDate.today()),
        "color": get_random_color()
    },
    "weekday": {  # 星期（周三）
        "value": weekday(),
        "color": get_random_color()
    },
    "words": {  # 彩虹屁
        "value": get_words(),
        "color": get_random_color()
    },
}
data.update(da)

# count = 0
# for user_id in user_ids:
#     res = wm.send_template(user_id, template_id, data)
#     print(data)
#     count += 1
# print("发送了" + str(count) + "条消息")

if __name__ == '__main__':

    try:
        client = WeChatClient(app_id, app_secret)
    except WeChatClientException as e:
        print('微信获取 token 失败，请检查 APP_ID 和 APP_SECRET，或当日调用量是否已达到微信限制。')
        exit(502)

    wm = WeChatMessage(client)
    count = 0
    try:
        for user_id in user_ids:
            print('正在发送给 %s, 数据如下：%s' % (user_id, data))
            res = wm.send_template(user_id, template_id, data)
            count += 1
    except WeChatClientException as e:
        print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
        exit(502)

    print("发送了" + str(count) + "条消息")

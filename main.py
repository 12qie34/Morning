from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
#   http://t.weather.itboy.net/api/weather/city/101270101
  url = "http://t.weather.itboy.net/api/weather/city/" + city
  res = requests.get(url).json()
#   weather = res['data']['list'][0]
  _province = res['cityInfo']['parent']
  _city = res['cityInfo']['city']
  tem = res['data']['wendu']
  wearther = res['data']['forecast'][0]
  return _province,_city,tem,werther['type'],weather['high'],weather['low']
#   return weather['weather'], math.floor(weather['temp']), weather['province'], weather['city'], math.floor(weather['low']), math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
_province, _city,temperature,wea, high, low = get_weather()
data = {"province":{"value":_province},"city":{"value":_city},"weather":{"value":wea},"temperature":{"value":temperature, "color":get_random_color()},"min_temperature":{"value":low},"max_temperature":{"value":high},"love_days":{"value":get_count(), "color":get_random_color()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
# data = {"city":{"value":city},"love_days":{"value":get_count(), "color":get_random_color()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)

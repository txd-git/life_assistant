import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
from fake_useragent import UserAgent
from .models import City
import json
import re

# Create your views here.
def index(request):
    return render(request, 'tq/get_location.html')


@csrf_exempt
def get_weather(request):
    # # 从前端传递的json字符串
    json_str = request.body
    # 序列化为json对象
    json_obj = json.loads(json_str)
    # 获取地址
    position = json_obj['my_address']

    # 判断取出的数据是否存在特殊字符和数字
    po_str = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '+']
    po_int = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for po in position:
        if po in po_str or po in po_int:
            result = {'code': 1001, 'error': '输入中存在特殊字符或者数字，请重新输入！'}
            return JsonResponse(result)
    # 判断数据库有没有要查询的城市
    try:
        city = City.objects.get(city_name=position)
    except Exception:
        result = {'code': 1002, 'error': '输入地址不存在，请重新输入该地址的上一级地址！'}
        return JsonResponse(result)
    # 拿到城市编号，爬取数据
    number = city.number
    url1 = 'http://www.weather.com.cn/weather/'
    url2 = '.shtml'
    # 拼接请求头
    url = url1 + number + url2
    # 请求头中加入解除反爬虫机制(包装User-Agent)
    headers = {'User-Agent':UserAgent().random}
    html = requests.get(url, headers=headers)
    # 使用utf-8的方式转化
    html.encoding = 'utf-8'
    htmlText = html.text
    # 使用BeautifulSoup解析
    soup = BeautifulSoup(html.text, 'html.parser')
    # 获取所要获取内容的大标签内容
    lis = soup.find_all('li', class_='sky')
    tianqi = []
    for li in lis:
        dic = {}
        # 获取日期
        h1_dates = li.find_all('h1')[0].get_text()
        # 获取温度
        p_weas = li.find_all('p', class_='wea')[0].get_text()
        # 获取天气
        p_tems = li.find_all('p', class_='tem')[0].get_text()
        # 获取风力
        p_wins = li.find_all('p', class_='win')[0].get_text()
        dic['date'] = h1_dates
        dic['weather'] = p_weas
        dic['templerature'] = p_tems
        dic['win'] = p_wins
        tianqi.append(dic)
    # 调用出行建议函数后要返回的数据中加入出行建议的数据
    we_advic = advics(tianqi[0]['weather'])
    tem_advice=t_advice(tianqi[0]['templerature'])
    result = {'code': 200, 'result': tianqi, "we_advic": we_advic,'tem_advice':tem_advice}

    return JsonResponse(result, safe=False)


@csrf_exempt
def get_addree(request):
    """
    根据传入的地址取出符合规则的地址,使用crsf装饰器，皮面跨站请求伪造攻击
    :param request:
    :return:
    """
    # 从前端传递的json字符串
    json_str = request.body
    # 序列化为json对象
    json_obj = json.loads(json_str)
    # 获得用户地址
    position = json_obj['address']
    shi = ""
    qu = ""
    # 对传来的地址操作，使其成为数据库中认识的区或者市。
    for i in range(len(position)):
        if position[i] == '省':
            for s in range(i, len(position)):
                if position[s] == '市':
                    shi = position[i + 1:s]
                    for q in range(s, len(position)):
                        if position[q] == '区' or position[q] == '县':
                            qu = position[s + 1:q]
    try:
        # 按最后获取的城市信息在数据库取城市编号
        city = City.objects.get(city_name=qu)
        city_name = qu
    except Exception:
        city_name = shi
        return JsonResponse({"address_name": city_name})
    return JsonResponse({"address_name": city_name})

def t_advice(template):
    """
    温度建议
    :param template: 温度
    :return:
    """

    tem = int(account(template))
    if tem>29:
        res = '建议您穿短袖'
        return res
    elif tem>=19:
        res = '昼夜温差大,建议您穿外套'
        return res
    elif tem>=9:
        res = '建议您穿秋衣秋裤'
        return res
    else:
        res = '室外温度低,建议您穿棉衣'
        return res


def advics(weather):
    """
    天气出行建议
    :param weather: 天气
    :return:
    """

    if '雪' in weather:
        res = '今天有雪，小心路滑'
        return res
    if '雨' in weather:
        res = '今天有雨，记得带伞'
        return res
    if '晴' in weather:
        res = '天气晴朗，适合户外有氧运动'
        return res
    if '云' in weather:
        res = '今天多云，合适运动'
        return res
    if '阴' in weather:
        res= '今天阴天，注意保暖'
        return res

def account(templerature):
    """
    计算平均温度
    :param templerature: 最高低温度
    :return: 平均温度
    """
    tems = templerature.split("℃")
    teml = tems[0].split("\n")[1]
    # 天气实时变化，可能不含有/，分情况讨论
    if '/' in teml:
        temm = teml.split("/")
        tem = int(temm[0])
        return tem
    else:
        tem = int(teml)
        return tem

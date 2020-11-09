from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import random
import requests
import json
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
from fake_useragent import UserAgent
from .models import History


# Create your views here.
def index(request):
    return render(request,'qiu/index.html')
def generate(request):
    """
    生成双色球方法
    :param request:
    :return:
    """
    list_computer = []
    while len(list_computer) < 6:
        num = random.randint(1, 33)
        if num not in list_computer:
            list_computer.append(num)
    blue_computer = random.randint(1, 16)
    # 生成随机双色球列表
    list_computer.append(blue_computer)
    # 由于发送过去的列表，参数加safe=False
    return JsonResponse(list_computer, safe=False)


# 爬期数功能
@csrf_exempt
def query(request):
    """
    查询期数方法
    :param request:
    :return:
    """
    result = {}
    # 接收数据，转化为py认识的数据，获取数值。
    json_str = request.body
    json_obj = json.loads(json_str)
    num = json_obj['number']
    # 判断传入的是能转成数字类型
    try:
        int(num)
    except Exception:
        result['code'] = 1003
        result['error'] = "主人，您不能输入字母或者字符，请重新输入"
        return JsonResponse(result)
    #输入不能为空
    if num == "":
        result['code'] = 1004
        result['error'] = "主人，您的输入不能为空"
        return JsonResponse(result)
    # 判断输入的不为负数
    if int(num) < 0:
        result['code'] = 1002
        result['error'] = "主人，您不能输入小于零的数字哟，请重新输入"
        return JsonResponse(result)
    # 判断输入的数据长度符合
    if len(num) != 5:
        result['code'] = 1001
        result['error'] = "主人，您输入的数据太长啦，请输入五位数的数字，请重新输入"
        return JsonResponse(result)
    # 输入符合要求，开始爬取内容,先查看数据库有没有内容.
    try:

        number = History.objects.get(nper=str(num))
        # 数据库有数据直接生成数据给前端
        result['nper'] = number.nper
        result['red_one'] = number.red_one
        result['red_two'] = number.red_two
        result['red_three'] = number.red_three
        result['red_four'] = number.red_four
        result['red_five'] = number.red_five
        result['red_six'] = number.red_six
        result['blue'] = number.blue
        result['time'] = number.time
        result['code'] = 200
        return JsonResponse(result)
    # 数据库没有这条记录，爬取数据加入数据库.
    except:
        # 调用爬取的函数
        datas = select(num)
        # 没爬到信息，彩票网没有这期彩票信息
        if not datas:
            result["code"] = 1003
            result["error"] = "主人，您输入的数字太大了，这期彩票开没开奖，请耐心等待"
            return JsonResponse(result)
        # 爬到数据生成结果，发送，添加信息到数据库
        for row in datas:
            tds = row.find_all('td')
            result['nper'] = tds[0].text
            result['red_one'] = tds[1].text
            result['red_two'] = tds[2].text
            result['red_three'] = tds[3].text
            result['red_four'] = tds[4].text
            result['red_five'] = tds[5].text
            result['red_six'] = tds[6].text
            result['blue'] = tds[7].text
            result['time'] = tds[-1].text
            result['code'] = 200
            # 数据库添加信息
            try:
                History.objects.create(nper=tds[0].text, red_one=tds[1].text, red_two=tds[2].text,
                                       red_three=tds[3].text, red_four=tds[4].text, red_five=tds[5].text,
                                       red_six=tds[6].text, blue=tds[7].text, time=tds[-1].text)
            # 数据库添加失败
            except:
                result["code"] = 1004
                result["error"] = "主人，系统开小差了，请重新输入"
                return JsonResponse(result)
        # 爬取到数据给数据
        return JsonResponse(result)


def select(num):
    """
    爬取数据
    :param num: 要爬取的期数
    :return: 带标签的数据
    """
    # 通过用户输入的期数形成url
    url = 'http://datachart.500.com/ssq/history/newinc/history.php?start=' + num + '&end=' + num
    #  生成随机的 User-Agent
    headers= {"User-Agent":UserAgent().random,}
    source = requests.get(url=url,headers=headers)
    # 获取响应内容
    source.encoding = source.apparent_encoding
    # 通过BeautifulSoup解析
    soup = BeautifulSoup(source.text, 'lxml')
    data = soup.find_all('tbody', id='tdata')
    datas = data[0].find_all('tr')
    # 获取节点信息及内容
    return datas

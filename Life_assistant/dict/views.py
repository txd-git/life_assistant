import json
import time
import random
from hashlib import md5
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from fake_useragent import UserAgent
from .models import Words


# Create your views here.

def check_word(request):
    return render(request, 'dict/check_word.html')

@csrf_exempt
def check_word_server(request):
    # 获取用户数据
    data = request.body
    dict = json.loads(data)
    word = dict['word']
    try:
        # 先从数据库尝试获取解释
        w = Words.objects.get(word=word)
    except Exception:
        # 获取失败，调用爬虫功能爬取解释
        spider = YdSpider()
        mean = spider.attack_yd(word)
        try:
            # 将解释添加值数据库
            Words.objects.create(word=word,mean=mean)
            result = {'code':200,'re':mean}
            return JsonResponse(result)
        except Exception:
            # 添加失败
            result = {'code':10314,'error':'网络丢失'}
            return JsonResponse(result)
    # 数据库获取成功数据，发送数据
    result = {'code': 200, 're': w.mean}
    return JsonResponse(result)

class YdSpider:
    def __init__(self):
        # url: url为F12抓包转到的地址(General->Request URL)
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            # 重点: 网站检查频率最高的是: Cookie Referer User-Agent
            "Cookie": "OUTFOX_SEARCH_USER_ID=-1168740771@10.108.160.102; OUTFOX_SEARCH_USER_ID_NCOO=1400714915.2659323; JSESSIONID=aaatGlvICvfe98k5NWWrx; ___rl__test__cookies=1599619646738",
            "Referer": "http://fanyi.youdao.com/",
            "User-Agent": UserAgent().random,
        }

    def get_ts_salt_sign(self, word):
        # ts salt
        ts = str(int(time.time() * 1000))
        salt = ts + str(random.randint(0, 9))
        # sign
        string = "fanyideskweb" + word + salt + "]BjuETDhU)zqSxf-=B#7m"
        s = md5()
        s.update(string.encode())
        sign = s.hexdigest()

        return ts, salt, sign

    def attack_yd(self, word):
        # 先获取ts salt sign
        ts, salt, sign = self.get_ts_salt_sign(word)
        data = {
            "i": word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            # 检查频率最高:salt sign
            "salt": salt,
            "sign": sign,
            "lts": ts,
            "bv": "e915c77f633538e8cf44c657fe201ebb",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }
        html = requests.post(url=self.url, data=data, headers=self.headers).text
        html = json.loads(html)

        return html['translateResult'][0][0]['tgt']


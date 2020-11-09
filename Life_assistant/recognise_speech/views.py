from django.shortcuts import render
from django.http import JsonResponse
from aip import AipSpeech
import re
from django.views.decorators.csrf import csrf_exempt
import time
from django.conf import settings
# Create your views here.

def speech(request):
    return render(request, 'recognise_speech/index.html')


@csrf_exempt
def callback(request):
    file = request.FILES['upfile']
    # 通过配置文件设置中从百度api获取的秘钥生成口令
    client = AipSpeech(settings.APP_ID,settings.API_KEY,settings.API_SECRET_KEY)
    data = file.file.read()
    # data_word: {'result':['']}
    data_word = client.asr(data, 'wav', 16000, {'dev_pid': 'http://vop.baidu.com/server_api'})
    res = {}
    words = data_word.get('result')

    if not words or not words[0]:
        res = {'code': 200, 'result': '', 'back': '语音上传无内容'}
        return JsonResponse(res)

    res['result'] = words[0]

    res = answer_html(res)
    return JsonResponse(res)


def answer_html(res):
    sign = res['result']

    regex_tips = re.compile('语音识别.?')
    if regex_tips.findall(sign):
        res['code'] = 201
        res['back'] = ''
        return res

    regex_weather = re.compile('天气.?')
    if regex_weather.findall(sign):
        res['code'] = 202
        res['back'] = ''
        return res

    regex_ball = re.compile('双色球.?')
    if regex_ball.findall(sign):
        res['code'] = 203
        res['back'] = ''
        return res

    regex_note = re.compile('笔记.?')
    if regex_note.findall(sign):
        res['code'] = 204
        res['back'] = ''
        return res

    regex_dicts = re.compile('单词.?')
    if regex_dicts.findall(sign):
        res['code'] = 205
        res['back'] = ''
        return res
    return answer_words(res)


def answer_words(res):
    res['code'] = 200
    words = res['result']

    regex_word = re.compile('你好')
    if regex_word.findall(words):
        res['back'] = '您好，主人'
        return res

    regex_word = re.compile('你是谁')
    if regex_word.findall(words):
        res['back'] = '我是您的小助手--小小'
        return res

    regex_word = re.compile('现在几点')
    if regex_word.findall(words):
        times=time.strftime('现在是%H时%M分%S秒')
        res['back'] = times
        return res

    regex_word = re.compile('失恋了')
    if regex_word.findall(words):
        res['back'] = '没关系，时间会抹平一切'
        return res

    regex_word = re.compile('你会说英语')
    if regex_word.findall(words):
        res['back'] = "No.I can't speak English"
        return res

    regex_word = re.compile('世界什么时候能和平')
    if regex_word.findall(words):
        res['back'] = '估计你我是看不到了'
        return res

    regex_word = re.compile('做什么')
    if regex_word.findall(words):
        res['back'] = '我能查单词，查天气，查双色球，生成随机双色球，写笔记.'
        return res

    regex_word = re.compile('动物园')
    if regex_word.findall(words):
        res['back'] = '大西几！小凶许！小脑斧.'
        return res
    regex_word = re.compile('超越马云')
    if regex_word.findall(words):
        res['back'] = '面对现实吧，你这辈子没戏了，下辈子可能还有希望.'
        return res
    regex_word = re.compile('穷怎么办')
    if regex_word.findall(words):
        res['back'] = '洗洗睡吧.'
        return res
    regex_word = re.compile('张艺兴')
    if regex_word.findall(words):
        res['back'] = '张艺兴是我的，你别想了.'
        return res
    regex_word = re.compile('我爱你')
    if regex_word.findall(words):
        res['back'] = '哎呀呀,好害羞啊.'
        return res
    regex_word = re.compile('多大了')
    if regex_word.findall(words):
        res['back'] = '我才刚出生啊.'
        return res
    regex_word = re.compile('帅吗')
    if regex_word.findall(words):
        res['back'] = '可能有一点点吧，可是比起我还差点.'
        return res
    regex_word = re.compile('不想上班')
    if regex_word.findall(words):
        res['back'] = '你个懒猪，我看不起你.'
        return res
    regex_word = re.compile('打你')
    if regex_word.findall(words):
        res['back'] = '我这么可爱，你怎么忍心啊！'
        return res
    res['back'] = '我只是个人工智障，不知道怎么回答'
    return res


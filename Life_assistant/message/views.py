import jwt
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from article.models import ArticlePost
from register.models import User_mian
from .models import Message
import json


def logging_check(func):
    def wrap(request, *args, **kwargs):
        # 获取请求头中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code': 403, 'error': 'please login'}
            return JsonResponse(result)
        # 校验token
        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithm='HS256')
        except Exception as e:
            print('check login is %s' % 3)
            result = {'code': 403, 'error': 'please login'}
            return JsonResponse(result)
        username = res['username']
        user = User_mian.objects.get(username=username)
        request.myuser = user
        return func(request, *args, **kwargs)

    return wrap

def get_user_by_request(request):
    # 从token中解析出用户名【登录的用户】
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        res = jwt.decode(token, settings.JWT_TOKEN_KEY)
    except Exception as e:
        print('get user jwt error %s' % e)
        return None
    username = res['username']
    return username

# Create your views here.
@logging_check
def send_message(request, id):
    if request.method != "POST":
        print("article_id")
        result = {"code": 10400, "error": "please uee POST"}
        return JsonResponse(result)
    json_obj = json.loads(request.body)
    try:
        content = json_obj['content']
    except Exception as e:
        return HttpResponse('**')
    p_id = json_obj.get('m_id', 0)
    try:
        article = ArticlePost.objects.get(id=id)
    except Exception:
        result = {'code': 1040, 'error': 'topic id error'}
        return JsonResponse(result)
    user = request.myuser
    Message.objects.create(article=article, content=content,
                           user=user,
                           p_id=p_id)
    return JsonResponse({'code': 200, "content": content})

from django.shortcuts import render
from django.http import JsonResponse
import jwt
from register.views import make_token
import json
import hashlib
from django.conf import settings
from register.models import User_mian
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index_view(request):
    """登录页面"""
    return render(request, 'login/loging.html')


def home_page_view(request):
    """主页面 """
    return render(request, 'login/home_page.html')


@csrf_exempt
def loging_view(request):
    # 获取用户名密码
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    password = json_obj['password']
    # 按照用户写的用户名在数据哭查找该用户是否存在
    try:
        old_user = User_mian.objects.get(username=username)
    except Exception:
        resuslt = {'code': 10101, "error": '用户名或密码错误'}
        return JsonResponse(resuslt)
    # 加密密码
    md5 = hashlib.md5()
    md5.update(password.encode())
    password_m = md5.hexdigest()
    # 判断密码是否正确
    if password_m != old_user.password:
        result = {'code': 10101, "error": '用户名或密码错误'}
        return JsonResponse(result)
    # 密码正确，签发token
    token = make_token(username)
    return JsonResponse({"code": "200", "username": username,
                         "data": {"token": token.decode()}})


# 验证状态函数
@csrf_exempt
def validation_state_view(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    token = json_obj['token']
    username = json_obj['username']
    # 根据请求头获取token
    # token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        # 判断有没有token
        result = {'code': 10115, 'error': '您还没有登录请登录'}
        return JsonResponse(result)
    try:
        # 判断本地储存的用户是不是我的用户
        user = User_mian.objects.get(username=username)
    except:
        result = {'code': 10116, 'error': '请您登录后再进行操作'}
        return JsonResponse(result)
    try:
        # 用自己的口令解析token
        res = jwt.decode(token, settings.JWT_TOKEN_KEY,
                         algorithms='HS256')
    except:
        result = {'code': 10115, 'error': '请您登录后再进行操作'}
        return JsonResponse(result)
    result = {'code': 200}
    return JsonResponse(result)

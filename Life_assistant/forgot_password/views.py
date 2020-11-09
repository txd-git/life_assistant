import hashlib
import json
import random

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from register.models import User_mian
from register.views import send_email, make_token


def forgot_password_view(request):
    return render(request, 'forgot_password/email_email_validation.html')

@csrf_exempt
def email_validation_view(request):
    """密码重置功能视图函数"""
    # 获取数据
    json_str = request.body
    json_obj = json.loads(json_str)
    validation = json_obj['validation']
    email = json_obj['email']
    password_1 = json_obj['password_1']
    password_2 = json_obj['password_2']
    username = json_obj['username']
    # 判断该用户是否存在
    if not email:
        result = {"code": 10117, "error": "邮箱不能为空"}
        return JsonResponse(result)
    try:
        # 按用户输入的email和用户名获取用户信息，判断用户信息的一致性
        user = User_mian.objects.get(username=username,email=email)
    except Exception:
        result = {"code":10113,"error":"用户名或邮箱错误"}
        return JsonResponse(result)
    # 判断两次密码是否一致
    if password_1!=password_2:
        result = {"code": 10114, "error": "密码不一致"}
        return JsonResponse(result)
    # 防止多次点击发送验证码
    cache_key = "smf_%s" % email
    old_code = cache.get(cache_key)
    # 判断有无验证码
    if not old_code:
        result = {"code": 10115, "error": "验证码为空"}
        return JsonResponse(result)
    # 判断验证码是否正确
    if int(validation) != old_code:
        result = {"code": 10116, "error": "验证码为空"}
        return JsonResponse(result)
    # 加密密码
    md5 = hashlib.md5()
    md5.update(password_1.encode())
    password_m = md5.hexdigest()
    # 修改密码
    user.password = password_m
    user.save()
    # 签发token
    token = make_token(user.username)
    return JsonResponse({"code": '200', "username": user.username,
                         "data": {"token": token.decode()}})
@csrf_exempt
def send_validation_view(request):
    # 获取前端传来的用户email账号
    json_str = request.body
    json_obj = json.loads(json_str)
    email = json_obj['email']
    # 判断用户该邮箱的可用性，是否存在
    try:
        user = User_mian.objects.get(email=email)
    except Exception:
        result = {'code': 10111, 'error': 'email error'}
        return JsonResponse(result)
    # 防止用户多次点击按钮重复发送验证码
    cache_key = 'smf_%s' % (email)
    old_code = cache.get(cache_key)
    if old_code:
        result = {'code': 10112, 'error': 'please later'}
        return JsonResponse(result)
    # 生成随机码
    code = random.randint(1000, 9999)
    # 放到缓存中,有效期75秒
    cache.set(cache_key, code, 75)
    # 调用发送emai的函数发送邮件
    send_email(email, code)
    return JsonResponse({'code': 200})

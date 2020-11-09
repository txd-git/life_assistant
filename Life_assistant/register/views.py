from django.shortcuts import render
from django.core.cache import cache
from .models import User_mian
import random
import json
import hashlib  # 加密密码
from django.http import JsonResponse
# 发送邮件所需,创建文本内容的邮件体
from email.mime.text import MIMEText
from email.header import Header
# email负责构造邮件，smtplib负责发送邮件
import smtplib
import jwt
from django.conf import settings
import time
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index_view(request):
    return render(request,'register/register.html')


@csrf_exempt
def register_view(request):
    """注册视图函数"""
    # 获取用户要注册的所有信息
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    nickname = json_obj['nickname']
    email = json_obj['email']
    sms = json_obj['sms']
    password_1 = json_obj['password_1']
    password_2 = json_obj['password_2']
    # 从内存中获取验证码
    cache_key = 'sms_%s' % email
    old_code = cache.get(cache_key)
    # 没有发送验证码
    if not old_code:
        result = {'code': 10103, 'error': '验证码为空'}
        return JsonResponse(result)
    # 验证验证码是否一样
    if int(sms) != old_code:
        result = {'code': 10102, 'error': '验证码错误'}
        return JsonResponse(result)
    # 验证用户名的长度
    if len(username) > 11:
        result = {"code": 10100, 'error': '用户名太长'}
        return JsonResponse(result)
    # 检查用户名是否可用（数据库查验）
    old_user = User_mian.objects.filter(username=username)
    if old_user:
        result = {"code": 10101, 'error': '用户名或密码错误'}
        return JsonResponse(result)
    # 处理密码
    if password_1 != password_2:
        result = {"code": 10104, 'error': '用户名或密码错误'}
        return JsonResponse(result)
    # 使用md5加密
    md5 = hashlib.md5()
    md5.update(password_1.encode())
    password_m = md5.hexdigest()
    # 创建用户注册信息
    try:
        User_mian.objects.create(username=username, nickname=nickname, email=email
                                 , password=password_m
                                 )
    except Exception:
        result = {"code": 10101, 'error': '网络异常,注册失败'}
        return JsonResponse(result)
    # 验证完毕，签发token
    token = make_token(username)
    return JsonResponse({"code": 200, "username": username,
                         "data": {"token": token.decode()}})


# 制作token,
def make_token(username, expire=3600 * 24):
    # 用配置文件设置的口令生成key
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    # 生成payload
    payload = {"username": username, 'exp': now + expire}
    # 使用django自带的jwt库生成token，（参数里注明加密方式--》哈希256位）
    return jwt.encode(payload, key, algorithm="HS256")


# 发送邮件的函数
def send_email(email, sim):
    mail_host = "smtp.qq.com"  # 设置服务器  smtp.163.com
    mail_user = "3323430956@qq.com"  # 用户名
    mail_pass = "navttksjpavucjaj"  # 口令
    # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message = MIMEText('您的验证码为%s,请勿转发给其他人,有效时间60秒.' % sim, 'plain', 'utf-8')
    # 发送者
    message['From'] = Header("智能小助手", 'utf-8')
    # 接收者
    message['To'] = Header(f"{email}", 'utf-8')
    subject = '[客户端验证]'
    message['Subject'] = Header(subject, 'utf-8')
    smtpObj = smtplib.SMTP()
    # 设置服务器，端口号
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    # 设置登录账号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(mail_user, email, message.as_string())

@csrf_exempt
def send_view(request):
    # 获取前端传来的用户email账号
    json_str = request.body
    json_obj = json.loads(json_str)
    email = json_obj['email']
    # 判断用户该邮箱的可用性，是否被注册
    user = User_mian.objects.filter(email=email)
    if user:
        result = {'code': 10112, 'error': '邮箱已经被注册'}
        return JsonResponse(result)
    # 防止用户多次点击按钮重复发送验证码
    cache_key = 'sms_%s' % (email)
    old_code = cache.get(cache_key)
    if old_code:
        # 从redis中取验证码，存在验证码则已经发送过验证码，
        result = {'code': 10112, 'error': '请稍后再来'}
        return JsonResponse(result)
    # 生成随机码
    code = random.randint(1000, 9999)
    print(code)
    # 放到缓存中,有效期75秒
    cache.set(cache_key, code, 75)
    # 调用发送验证码函数发送验证码
    send_email(email, code)
    return JsonResponse({'code': 200})
from django.shortcuts import render, redirect
# from comment.models import Comment
from .models import ArticlePost
from message.models import Message
from register.models import User_mian
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json, time, jwt
from django.conf import settings
from django.core.paginator import Paginator

# 装饰器
from message.views import logging_check,get_user_by_request


# Create your views here.
def article_list(request):
    if request.method == 'GET':
        article_list = ArticlePost.objects.all()
        # 获取url中的页码
        art_list = []
        for item in article_list:
            dict = {}
            dict['id'] = item.id
            dict['title'] = item.title
            dict['body'] = item.body
            dict['total_views'] = item.total_views
            art_list.append(dict)
        paginator = Paginator(art_list, 5)
        cur_page = request.GET.get('page', 1)
        page = paginator.page(cur_page)
        return render(request, 'article/list.html', locals())


# 文章详情
def article_detail(request, id):
    if request.method == 'GET':
        try:
            data = ArticlePost.objects.get(id=id)
            all_messages = Message.objects.filter(article=id)
        except Exception as e:
            return HttpResponse('未查到此内容')
        # 获取评论回复信息
        result = get_words(all_messages)
        data.total_views += 1
        data.save(update_fields=['total_views'])
        return render(request, 'article/detail.html', locals())


# 删除
def article_delete(request, id):
    if request.method == "POST":
        try:
            data = ArticlePost.objects.get(id=id)
        except Exception:
            return HttpResponse('未查到此内容')
        visitor_name = get_user_by_request(request)
        name = data.author.username
        if visitor_name == name:
            data.delete()
            return JsonResponse({'code': 200})
        else:
            return JsonResponse({"code": 404})


# 编辑判断
def edit(request, id):
    if request.method == "POST":
        try:
            data = ArticlePost.objects.get(id=id)
        except Exception:
            return HttpResponse('未查到此内容')
        visitor_name = get_user_by_request(request)
        if visitor_name == data.author.username:
            return JsonResponse({'code': 200, "id": data.id})
        else:
            return JsonResponse({"code": 404})


# 开始编辑
def update(request, id):
    if request.method == "GET":
        try:
            article = ArticlePost.objects.get(id=id)
        except Exception :
            return HttpResponse('未查到此内容')
        return render(request, 'article/update.html', locals())
    elif request.method == "POST":
        try:
            data = ArticlePost.objects.get(id=id)
        except Exception as e:
            return HttpResponse('未查到此内容')
        data.title = request.POST.get('title')
        data.body = request.POST.get('body')
        data.save()
        return HttpResponseRedirect('/article/artlist')


# p匹配评论和回复
def get_words(all_messages):
    msg_list = []
    r_dict = {}
    p_count = 0
    for msg in all_messages:
        if msg.p_id:
            r_dict.setdefault(msg.p_id, [])
            r_dict[msg.p_id].append({'msg_id': msg.id, 'content': msg.content,
                                     'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S')
                                     })
        else:
            msg_list.append({'id': msg.id, 'content': msg.content,
                             'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                             'reply': []})
            p_count += 1

    for m in msg_list:
        if m['id'] in r_dict:
            m['reply'] = r_dict[m['id']]
    result = {"msg": msg_list, "p_count": p_count}
    return result


# 发帖认证
@logging_check
def log_dec(request):
    if request.method == "GET":
        return JsonResponse({'code': 200})


def create(request, username):
    if request.method == "GET":
        return render(request, 'article/create.html')

    elif request.method == "POST":
        user = User_mian.objects.get(username=username)
        title = request.POST.get('title')
        body = request.POST.get('body')
        # 数据入库
        ArticlePost.objects.create(title=title, body=body, author=user)
        return HttpResponseRedirect('/article/artlist')


# 按浏览量排序显示
def total_views(request):
    if request.method == 'GET':
        article_list = ArticlePost.objects.all().order_by('-total_views')
        art_list = []
        for item in article_list:
            dict = {}
            dict['id'] = item.id
            dict['title'] = item.title
            dict['body'] = item.body
            dict['total_views'] = item.total_views
            dict['img'] = str(item.img)
            art_list.append(dict)
        return JsonResponse(art_list, safe=False)

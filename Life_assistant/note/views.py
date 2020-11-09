from django.shortcuts import render
import json
from register.models import User_mian
from .models import Note
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
import time


def page_add_note(request):
    """添加日记返回页面视图"""
    return render(request, 'note/add_note.html')


def page_update_note(request, nid):
    """修改日记页面视图"""
    return render(request, 'note/update_note.html')


def all_notes(request):
    """日记页面视图"""
    return render(request, 'note/all_note.html')


@csrf_exempt
def all_note_view(request):
    """查看日记（日记列表）"""
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    try:
        # 尝试用数据库获取该用户信息
        user = User_mian.objects.get(username=username)
    except Exception:
        result = {'code': 10301, 'error': '获取用户失败'}
        return JsonResponse(result)

    # 拿到该用户所有可见的日记
    all_note = Note.objects.filter(user=user, is_active=1).order_by('created_time')
    # 调用生成日记列表数据函数生成json数据
    result = note_list(all_note)
    return JsonResponse(result)


def note_list(all_note):
    """获取日记列表"""
    notes = []
    # 遍历用户的所有日记
    for note in all_note:
        # 形成每一个日记字典
        d = {}
        d['id'] = note.id  # 日记对应id
        d['title'] = note.title  # 日记对应的标题
        d['content'] = note.content[:20]  # 给前段显示的是日记内# 日记对应的标题容，日记前20个字
        # 日记的创建时间
        d['created_time'] = note.created_time.strftime('%Y-%m-%d %H:%M:%S')
        # 日记的修改时间
        d['updated_time'] = note.updated_time.strftime('%Y-%m-%d %H:%M:%S')
        notes.append(d)
    res = {'code': 200, 'data': notes}
    return res


@csrf_exempt
def add_note_view(request):
    """
    添加日记函数
    :param request:
    :return:
    """
    json_str = request.body
    json_obj = json.loads(json_str)
    # 获取用户日记的标题，内容
    title = json_obj['title']
    content = json_obj['content']
    username = json_obj['username']
    # 判断添加的内容
    if not title or not content:
        result = {'code': 10341, 'error': '内容或标题不能为空'}
        return JsonResponse(result)
    # 获取用户
    user = User_mian.objects.get(username=username)
    try:
        # 添加日记
        Note.objects.create(title=title, content=content, user=user)
    except Exception:
        # 添加失败
        result = {'code': 10305, 'error': '系统开小差了'}
        return JsonResponse(result)
    # 添加成功返回200
    result = {'code': 200}
    return JsonResponse(result)


@csrf_exempt
def delete_note_view(request, nid):
    """
    删除日记函数
    :param request:
    :return:
    """
    # 获取要还是删除的日记id
    try:
        # 用日记id获取该日记
        note = Note.objects.get(id=nid)
    except Exception:
        result = {'code': 10306, 'error': '找不到该日记'}
        return JsonResponse(result)
    # 修改日记的可见即删除日记
    note.is_active = False
    note.save()
    return HttpResponseRedirect('/note/all_notes')


@csrf_exempt
def update_note_view(request):
    """修改日记函数"""
    # 获取到要修改日记的id，修改后的标题，内容
    json_str = request.body
    json_obj = json.loads(json_str)
    note_id = json_obj['id']
    title = json_obj['title']
    content = json_obj['content']
    try:
        # 按id获取该日记
        note = Note.objects.get(id=note_id)
    except Exception:
        result = {'code': 10304, 'error': '获取日记失败'}
        return JsonResponse(result)
    # 判断内容是否修改
    if note.title == title or note.content == content:
        result = {'code': 10315, 'error': '您的标题或日记未修改'}
        return JsonResponse(result)
    # 修改日记
    note.title = title
    note.content = content
    note.save()
    result = {'code': 200}
    return JsonResponse(result)


def one_note_view(request, nid):
    """给修改日记改回该日记的标题和内容"""
    try:  # 从地址栏获取id后，尝试从数据库获取该日记
        note = Note.objects.get(id=nid)
    except Exception:
        result = {'code': 10308, 'error': '获取日记失败'}
        return JsonResponse(result)
    # 获取该日记的标题和内容
    title = note.title
    content = note.content
    # 获取成功，返回给前端 该id对应日记的标题和内容
    result = {'code': 200, 'title': title, 'content': content}
    return JsonResponse(result)

# def send_data_view(request):
#     """给前段日记主页面返回当日日期"""
#     data_time = time.strftime('%Y-%m-%d')
#     result = {'code': 200, 'data': data_time}
#     return JsonResponse(result)

# -*-coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User  # django 自带后台管理模块
from django.contrib import auth


# 主页
from meetingsApp.models import MyUser


def index(req):
    username = req.session.get('username', '')
    content = {'active_menu': 'homepage', 'user': username}
    return render_to_response('index.html', content)  # 将数据返回到前台


# 注册
def regist(req):
    if req.session.get('username', ''):  # 获取session用来判断用户是否登录
        return HttpResponseRedirect('/')
    status = ""
    if req.POST:
        username = req.POST.get("username", "")  # 从前台获得用户注册信息，判断，存入数据库
        if User.objects.filter(username=username):
            status = "user_exist"
        else:
            password = req.POST.get("password", "")
            repassword = req.POST.get("repassword", "")
            if password != repassword:
                status = "re_err"
            else:
                newuser = User.objects.create_user(username=username, password=password)
                newuser.save()
                new_myuser = MyUser(user=newuser, phone=req.POST.get("phone"))
                new_myuser.save()
                status = "success"
                return HttpResponseRedirect("/login/")
    return render_to_response("regist.html", {"active_menu": "hompage", "status": status, "user": ""},
                              context_instance=RequestContext(req))


# 登录
def login(req):
    if req.session.get('username', ''):
        return HttpResponseRedirect('/')
    status = ""
    if req.POST:
        username = req.POST.get("username", "")
        password = req.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(req, user)
            req.session["username"] = username  # 保存登录会话
            return HttpResponseRedirect('/')
        else:
            status = "not_exist_or_passwd_err"
    return render_to_response("login.html", {"status": status}, context_instance=RequestContext(req))


# 退出登录
def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/')

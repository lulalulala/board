# _*_ encoding:utf-8 _*_
from django.shortcuts import render, RequestContext, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from . import models
from . import forms
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.admin import User
from django.contrib.auth.decorators import login_required
from django.db.utils import InternalError
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count


#首页
def index(request):
    if request.user.is_authenticated():
        userinfo = request.user.username
        username = User.objects.get(username=userinfo)
        user = models.Users.objects.get(username=username)
    else:
        pass
    articles = models.All_Article.objects.all()
    nickname = []

    #articles_replay = models.All_Article.objects.annotate(num_posts=Count('replay'))

    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    for n in contacts:
        nick = models.Users.objects.get(username=n.user)
        nickname.append(nick)
    art_name = list(zip(articles, nickname))

    template = get_template('index.html')
    html = template.render(locals())
    return HttpResponse(html)



#注册页面
def registration(request):
    if request.method == 'POST':
        print('lslsl')
        post_form = forms.LoginForm(request.POST)
        if post_form.is_valid():
            try:
                user = User.objects.create_user(username=request.POST.get('username'), password=request.POST.get('password'))
                users = models.Users.objects.create(username=user)
                user.save()
            except:
                messages.add_message(request, messages.WARNING, '该用户名已被注册')
            print('success')
            messages.add_message(request, messages.SUCCESS, '注册成功')
            return HttpResponseRedirect('/login')      #注册成功跳转页面
        else:
            messages.add_message(request, messages.WARNING, '请填写完整')
    else:
        post_form = forms.PostForm()


    template = get_template('registration_form.html')
    reg = RequestContext(request)
    reg.push(locals())
    html = template.render(reg)

    return HttpResponse(html)



#登陆
def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST.get('username')
            login_password = request.POST.get('password')
            user = authenticate(username=login_name, password=login_password)
            print(user)
            if user is not None:
                print('lll')
                if user.is_active:
                    auth.login(request, user)
                    print('success')
                    username = request.user.username
                    messages.add_message(request, messages.SUCCESS, '成功登陆')
                    return HttpResponseRedirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '帐号尚未启用')
            else:
                messages.add_message(request, messages.WARNING, '用户名输入错误')
        else:
            messages.add_message(request, messages.INFO, '请检查输入的字段内容是否错误')
    else:
        login_form = forms.LoginForm()

    template = get_template('login.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)
    response = HttpResponse(html)

    return response

#注销
def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, '成功注销')
    return redirect('/')



@login_required(login_url='/login/')
#发文
def post(request):                     #发文
    print('lll')
    if request.user.is_authenticated():
        post_user = request.user.username
        username = User.objects.get(username=post_user)
        user = models.All_Article(user=username)
        if request.method == 'POST':
            post = forms.PostArticle(request.POST, instance=user)
            if post.is_valid():
                articles = models.All_Article.objects.create(title=request.POST.get("title"),article=request.POST.get("article"),user=username, replay_time=datetime.now())

                articles.save()
                messages.add_message(request, messages.INFO, '成功')
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.INFO, '请检查您是否填写完整')
        else:
            post = forms.PostArticle()
    else:
        return HttpResponseRedirect('/login/')

    template = get_template('post.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)

    return HttpResponse(html)



#文章页
def article(request, id):
    art = models.All_Article.objects.get(id=id)
    art_user = models.Users.objects.get(username=art.user)
    try:
        replay = models.Replay.objects.filter(all_article=art)
        replay_nickname=[]
        replay_idlist=[]
        for i in replay:
            replay_user = models.Users.objects.get(username=i.user)
            replay_id = User.objects.get(username=i.user)
            replay_idlist.append(replay_id)
            replay_nickname.append(replay_user)

        paginator = Paginator(replay, 5)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        replay_list=list(zip(contacts,replay_nickname, replay_idlist))
    except:
        replay=None

    if request.user.is_authenticated():
        username = User.objects.get(username=request.user.username)
        user = models.Users.objects.get(username=username)
        if request.method == 'POST':
            post_replay = models.Replay(all_article=art)
            post = forms.ReplayForm(request.POST)
            if post.is_valid():
                print(request.POST.get('user'))
                #post.save()
                print(art.id)
                rp = models.Replay(all_article=art,text=request.POST.get("text"), user=username)
                art.replay_time=datetime.now()
                rp.save()
                art.save()
                messages.add_message(request, messages.INFO, '成功')
                return HttpResponseRedirect('/article/%s' % (id))
            else:
                messages.add_message(request, messages.INFO, '请检查是否填写完整')
        else:
            post = forms.ReplayForm()
    else:
        return HttpResponseRedirect('/login')

    template = get_template('article.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)

    return HttpResponse(html)

#收藏操作
def obj_collection(request, art_id):
    if request.user.is_authenticated():
        userinfo = request.user.username
        try:
            art = models.All_Article.objects.get(id=art_id)
        except:
            art = None
        try:
            username = User.objects.get(username=userinfo)
            col = models.Collection.objects.get(user=username)
        except:
            col = models.Collection.objects.create(user=username)

        if art is not None:
            col.article.add(art)
            col.save()

    else:
        return redirect('/login')

    url = '/article/' + art_id
    print(url)
    return redirect(url)




#用户个人信息修改页面
@login_required(login_url='/login/')
def userinfo(request):
    if request.user.is_authenticated():
        userinfo =request.user.username
        username = User.objects.get(username = userinfo)
        user = models.Users.objects.get(username = username)
        if request.method == 'POST':
            post = forms.PostForm1(request.POST)
            if post.is_valid():
                nickname = request.POST.get('nickname')
                message = request.POST.get('message')
                print('111111')
                models.Users.objects.filter(username=username).update(nickname=nickname,message=message)

                messages.add_message(request, messages.INFO, '修改成功')
            else:
                messages.add_message(request, messages.INFO, '请填写完整')
        else:
            post = forms.PostForm1()
    else:
        return redirect('/login/')

    template = get_template('userinfo.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)
    response = HttpResponse(html)
    return HttpResponse(html)

#修改密码
@login_required(login_url='/login/')
def change_psw(request):
    if request.user.is_authenticated():
        userinfo = request.user.username
        username = User.objects.get(username = userinfo)
        user = models.Users.objects.get(username = username)
        if request.method == 'POST':
            post = forms.ChangePSW(request.POST)
            if post.is_valid():
                oldpsw = request.POST.get('oldpass')
                newpsw = request.POST.get('newpass')
                checkpsw = request.POST.get('checkpass')
                if newpsw == checkpsw:
                    usr = authenticate(username=userinfo, password=oldpsw)
                    if usr is not None and usr.is_active:
                        usr.set_password(newpsw)
                        usr.save()
                        messages.add_message(request, messages.SUCCESS,'修改成功')
                    else:
                        messages.add_message(request, messages.WARNING,'旧密码输入错误')
                else:
                    messages.add_message(request, messages.WARNING,'密码重复输入错误')
            else:
                messages.add_message(request,messages.WARNING,'请检查输入内容格式是否错误')
        else:
            post = forms.ChangePSW()
    else:
        return redirect('/login')
    template = get_template('change_psw.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)
    response = HttpResponse(html)

    return HttpResponse(html)


#收藏页面
@login_required(login_url='/login/')
def collection(request):
    if request.user.is_authenticated():
        userinfo = request.user.username
        username = User.objects.get(username=userinfo)
        user = models.Users.objects.get(username=username)
        collection = models.Collection.objects.get(user=username)
        art = []
        for col in collection.article.all():
            print(col)
            col_art = models.All_Article.objects.get(title=col)
            art.append(col_art)
    else:
        return redirect('/login/')

    template = get_template('collection.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)

    return HttpResponse(html)

#个人文章页面
@login_required(login_url='/login/')
def user_article(request):
    if request.user.is_authenticated():
        username = request.user.username
        user = User.objects.get(username=username)
        articles = models.All_Article.objectes.filter(user=user)
    else:
        return redirect('/login/')
    template = get_template('user_article.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)

    return HttpResponse(html)


#个人回复页面
@login_required(login_url='/login/')
def user_replay(request):
    if request.user.is_authenticated():
        username = request.user.username
        user = User.objects.get(username=username)
        replay = models.Replay.objects.filter(user=user)
        articles = models.All_Article.objects.all()
    else:
        return redirect('/login/')
    template = get_template('user_replay.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)

    return HttpResponse(html)



# Create your views here.


"""message_board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from mysite import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),                        #首页
    url(r'^register', views.registration),         #注册页面
    url(r'^login$', views.login),                  #登陆页面
    url(r'^logout$', views.logout),                #注销
    url(r'^userinfo/\d+$', views.user_article),     #用户个人信息页面
    url(r'^userinfo/\d+/userinfo', views.userinfo), #修改个人信息
    url(r'^userinfo/\d+/user_replay', views.user_replay), #个人回复
    url(r'^userinfo/\d+/change_psw', views.change_psw),  #更改密码
    url(r'^userinfo/\d+/post$', views.post),       #发文页面
    url(r'^article/(\d+)$',views.article),         #文章页面
    url(r'^article/(\d+)/col$', views.obj_collection),   #文章收藏
    url(r'^userinfo/\d+/collection$', views.collection),   #个人收藏页面
    url(r'^userinfo/\d+/replay$', views.user_replay),   #个人回复页面

]

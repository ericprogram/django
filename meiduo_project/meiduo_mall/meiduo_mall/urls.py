"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),

    # 用户模块 users
    # Django1.x跟Django2.x版本区别:
    # 路由层1.x用的是url,而2.x用的是path,
    # 2.x版本中的path的第一个参数不再是正则表达式,而是些什么就匹配什么,是精准匹配,
    # 当使用2.x不习惯的时候, 2.x还有一个叫re_path , 2.x中的re_path就是1.x的url
    # path('', include(('users.urls', "users"), namespace='users')),
    re_path(r'^', include(('users.urls', "users"), namespace='users')),

    # 图形验证码 verifications
    re_path(r'^', include(('verifications.urls', 'verifications'), namespace='verifications')),

    # 首页模块
    re_path(r'^', include(('contents.urls', 'contents'), namespace='contents')),



]


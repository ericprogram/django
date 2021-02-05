"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),  # 后台管理站点路由

    # url(r'^', include('users.urls')),  # 把users子应用中的所有路由添加到总路由/根路由中

    # url(r'^users/index/$', views.index),  # 只在总里面去定义路由

    url(r'^users/', include('users.urls', namespace='users')),  # 总里面写一段

    url(r'^', include('request_response.urls', namespace='request_response')),  # 演示请求和响应模块

    url(r'^', include('classview.urls')),  # 类视图模块
]

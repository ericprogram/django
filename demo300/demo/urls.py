"""demo URL Configuration

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
from django.urls import path,include
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 将users应用下的所有路由导入到工程路由总路由中：
    # 总路由里面写应用路径的前缀，总 + 子
    url(r'^users/', include('users.urls',namespace='users')),

    # 只在总路由里编写路由代码,不建议使用 :总
    # url(r'^user/index/$',views.index),

    # 所有路由信息都写在应用中：总里面只做导入
    # url(r'^',include('users.urls')),
    url(r'^',include('request_response.urls',namespace='request_response')),

]

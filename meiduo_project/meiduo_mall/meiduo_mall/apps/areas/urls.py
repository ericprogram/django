from django.conf.urls import url

from . import views

# Author: hmchen
# DATE  : 2021/2/28 18:27


urlpatterns = [
    # 省市区数据查询
    url(r'^areas/$', views.AreasViwe.as_view(),name='areas'),
]

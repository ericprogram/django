from django.conf.urls import url

from . import views

urlpatterns = [
    # 获取qq登陆url
    url(r'^qq/authorization/$', views.QQAuthURLView.as_view())
]
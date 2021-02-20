from django.conf.urls import url

from . import views

urlpatterns = [
    # 获取qq登陆url
    url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),

    # QQ登陆成功后回调处理
    url(r'^oauth_callback$', views.QQAuthView.as_view()),

]
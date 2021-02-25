from django.conf.urls import url


from . import views


urlpatterns = [
    # 注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),

    # 用户名是否重复注册
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view(),
        name='usernamecountview'),

    # 手机号是否重复注册
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view(), name='mobilecountview'),

    # 用户登陆
    url(r'^login/$', views.LoginView.as_view(), name='login'),

    # 用户退出登陆
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    # 用户中心
    url(r'^info/$', views.InfoView.as_view(), name='info'),

    # 设置用户邮箱
    url(r'^emails/$', views.EmailView.as_view(), name='emails'),

    # 邮箱激活
    url(r'^emails/verification/$', views.EmailVerifyView.as_view(), name='emails_verification'),

]
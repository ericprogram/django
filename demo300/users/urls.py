from django.conf.urls import url
from users import views



app_name = 'users'

# 应用中所有路径都写在此列表中
# http://127.0.0.1:8003/users/index/
urlpatterns =[
    # url(正则，视图名)
    # url(r'^index/$',views.index),
    # url(r'^test/&',views.test2),


    # http://127.0.0.1:8003/users/index/
    url(r'^users/index/$',views.index,name='query_par'),

    # 以下是为了测试路径匹配顺序，自上而下

    url(r'^users/say/$',views.say),
    url(r'^users/sayhello/$',views.say_hello),



]
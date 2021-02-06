from django.conf.urls import url
from request_response import views

app_name = 'request_response'
urlpatterns = [

    # url(路径，函数名，name=给路由取别名)

    url('^weather/(?P<city>[a-z]+)/(?P<year>\d{4})/$',views.weather),
    # 获取查询字符串
    url(r'^get_query_params/$',views.get_query_params,name='query_par'),
    # 获取请求体非表单数据 form表单
    url(r'^get_form_date/$',views.get_form_date),
    # 获取请求体非表单数据 json
    url(r'^get_json/$',views.get_json),
    # response响应对象
    url(r'^response_test/$',views.response_test),
    # 重定向
    url(r'^redirect_test/$',views.redirect_test),
    # cookie的使用
    url(r'^cookie_test/$',views.cookie_test),



]
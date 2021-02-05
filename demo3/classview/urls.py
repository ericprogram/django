from classview import views
from django.conf.urls import url


app_name ='classview'

urlpatterns = [
    # 类视图
    # url(类名，函数名)
    # 类视图as_view作用:
    # 将类视图中的方法转换为函数
    # 它里面dispatch方法可以根据本次请求方法动态查找类中和请求方法同名但小写的方法
    # url(r'^demoview/$',view,name='classview'),
    url(r'^demoview/$',views.DemoView.as_view(),name='classview'),

    # 直接用装饰器装饰as_view 方法返回的view函数，只不过这样把类视图中的所有方法都装饰
    # url(r'^demoview/$',views.my_decorator(views.DemoView.as_view()),name='classview'),

]

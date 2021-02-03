from django.conf.urls import url
from . import views
# 应用中所有路径都写在此列表中

urlpatterns =[
    # url(正则，视图名)
    url(r'^index/$',views.index),
]
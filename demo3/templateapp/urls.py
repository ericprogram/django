from django.conf.urls import url
from templateapp import views

app_name ='templateapp'

urlpatterns = [
    url(r'^templateapp/$',views.TempView.as_view(),name='template_app'),
    # url(r'^demoview/$', views.DemoView.as_view(), name='classview'),
]

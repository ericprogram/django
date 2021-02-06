from django.conf.urls import url
from templateapp import views

app_name ='templateapp'

urlpatterns = [
    url(r'^templateapp/$',views.TempView.as_view(),name='template_app'),
    # url(r'^demoview/$', views.DemoView.as_view(), name='classview'),
    url(r'^base/$',views.TempBaseView.as_view(),name='template_base'),
    url(r'^child/$',views.TempChildView.as_view(),name='template_child'),
    url(r'^jinja2test/$',views.Jinja2View.as_view(),name='jinja2_test'),

]

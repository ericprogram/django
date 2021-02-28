from django import http
from django.shortcuts import render
from django.views import View

from . models import Area
from meiduo_mall.utils.response_code import RETCODE

# Create your views here.


class AreasViwe(View):
    """省市区数据查询"""

    def get(self, request):

        # 获取查询参数area_id
        area_id = request.GET.get('area_id')

        # 判断是否有area_id
        # 如果前端没有传area_id,说明它想查询所有省
        if area_id is None:
            # 查询所有省数据
            province_qs = Area.objects.filter(parent=None)
            # 此列表用来装每一个省的字典
            province_list = []
            # 遍历查询集，将查询集中的模型转成字典并添加到列表中
            for province_model in province_qs:
                province_list.append({
                    'id': province_model.id,
                    'name': province_model.name
                })

            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'province_list': province_list})
        else:
            # 如果前端传了area_id, 说明它想查指定区域的下级所有行政区
            pass






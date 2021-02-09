from django.contrib import admin

# Register your models here.
from booktest.models import Bookinfo, HeroInfo


class BookInfoAdmin(admin.ModelAdmin):
    """ 模型站点管理类 """
    list_display = ['id', 'bread_unit', 'btitle', 'bpub_date','pub_date', 'bread', 'bcomment','is_delete', 'hero_list']  # 列表页显示那些数据
    actions_on_top = True
    actions_on_bottom = True
    # 1. 显示字段
    # fields = ['btitle', 'bpub_date']

    # 2.分组显示
    fieldsets = (
        ('基本', {'fields': ['btitle', 'bpub_date']}),
        ('高级', {
            'fields': ['bread', 'bcomment'],
            'classes': ('collapse',)  # 是否折叠显示
        })
    )

# @admin.register(HeroInfo) 相当于 admin.site.register(HeroInfo)

@admin.register(HeroInfo)
class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'hname', 'hcomment']
    list_filter = ['hname', 'hgender', 'hcomment']  #  右侧过滤拦
    search_fields = ['hname']  # 搜索框 属性如下，用于对指定字段的值进行搜索，支持模糊查询。列表类型，表示在这些字段上进行搜索


# admin.site.site_header 设置网站页头
# admin.site.site_title 设置页面标题
# admin.site.index_title 设置首页标语

admin.site.site_header = 'Eric学习站点'
admin.site.site_title = 'Eric学习Django管理'
admin.site.index_title = '欢迎访问Eirc的书城'

# 注册模型到站点中
admin.site.register(Bookinfo, BookInfoAdmin)
# admin.site.register(HeroInfo)







"""定义learning_logs的URL模式"""

from django.conf.urls import url

from . import views  # 从当前url模块所在文件夹导入视图

app_name = 'learning_logs'

urlpatterns = [  # 包含可在learning_logs中请求的网页
    # 主页
    url(r'^$', views.index, name='index'),  # r'^$'指基础URL

    # 显示所有主题
    # 指基础URL后面跟着topics. topics后面最多加一个/
    url(r'^topics/$', views.topics, name='topics'),  

    # 测试用的网页
    url(r'^test/$', views.test, name='test'),

    # 特定主题的详细页面
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    
    # 用于添加新主题的网页
    url(r'^new_topic/$', views.new_topic, name='new_topic'),

    # 用于添加新条目的页面
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),

    # 用于编辑条目的页面
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]
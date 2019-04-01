"""为应用程序users定义URL模式"""

from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # 登录界面
    # 正则表达式指定localhost:8000/users/login/与登录界面匹配
    # login将请求发送给Django默认视图login(注意视图实参是login, 而不是views.login)
    # 由于没有自己编写视图函数, 我们传递一个字典告诉Django去哪里寻找模板,
    # 这个模板包含在应用程序users中, 而不是learning_logs中
    url(r'^login/$', LoginView.as_view(template_name='users/login.html'),
        name='login'),
    
    # 注销
    url(r'^logout/$', views.logout_view, name='logout'),

    # 注册页面
    url (r'^register/$', views.register, name='register')
]
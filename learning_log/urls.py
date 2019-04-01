"""learning_log URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    # admin.site.urls定义了可在管理网站中请求的所有URL
    path(r'admin/', admin.site.urls),
    url(r'users/', include('users.urls', namespace='users')),
    # 包含模块learning_logs.urls,
    # # 实参namespace让我们能够将learning_logs的URL同项目中的其他URL区分开来
    url(r'', include('learning_logs.urls', namespace='learning_logs')),
    # (r'^accounts/login/$', LoginView.as_view(template_name='users/login.html'),
    #     name='login'),
]

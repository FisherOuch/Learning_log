from django.shortcuts import render
from django.http import HttpResponseRedirect  # 用来在用户提交主题后将用户重定向到网页topics
from django.urls import reverse
from django.template import RequestContext  # 为了在html中使用url.is_authenticated
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

# Create your views here.
def logout_view(request):
    """注销用户"""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
    """注册新用户"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录, 再重定向到主页
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))
    
    context = {'form': form}
    return render(request, 'users/register.html', context)
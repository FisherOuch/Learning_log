from django.shortcuts import render
# HttpResponseRedirect用来在用户提交主题后将用户重定向到网页topics
# 导入Http404, 并在用户请求他不能查看的主题时引发这个异常
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.template import RequestContext  # 为了在html中使用url.is_authenticated
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def check_topic_owner(request, topic):
    if topic.owner != request.user:
    # 禁止用户通过输入URL来访问其他用户的条目,
    # 如果不是主题的所有者, 则引发Http404异常
        raise Http404

def index(request):
    """学习笔记的主页"""
    # request是指原始请求对象
    # ''内的部分可用于创建网页的模板
    return render(request, 'learning_logs/index.html')  # 为主页编写视图

# 将login_required()作为装饰器用于视图函数topics(),
# 让Python在运行topics()的代码前先运行login_required()的代码
@login_required
# 检查用户是否已登录, 仅当用户已登录时, Django才运行topics()的代码.
# 如果用户未登录, 就重定向到登录界面, 要实现这一功能, 需要先修改settings.py
def topics(request):
    """显示所有的主题"""
    # 将返回的查询集存储在topics中
    # filter(owner=request.user)筛选只属于当前用户的Topic对象
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    # 创建字典, 值是要发送给模板的数据, 键是在模板中用来访问数据的名称
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def test(request):
    """测试超链接用的网页"""
    return render(request, 'learning_logs/test.html')  # 为主页编写视图

@login_required
def topic(request, topic_id):
    """显示特定的主题, 即条目明细"""
    # 将返回的查询集存储在topics中
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户
    check_topic_owner(request, topic)
    entries = topic.entry_set.order_by('date_added')
    # 创建字典, 值是要发送给模板的数据, 键是在模板中用来访问数据的名称
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':  # 确定方法是GET还是POST
        # 只是从服务器读取数据的页面, 使用GET请求
        # 未提交数据: 创建一个新表单(无论是GET还是其他类型的请求, 返回空表单都没问题)
        form = TopicForm()
    else:
        # 在用户需要通过表单提交信息时, 通常使用POST请求
        # POST提交的数据, 对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            # 如果表单的信息都是有效的(默认都是必填的)
            # 将表单写入数据库
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # 将用户的浏览器重定向到页面topics
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    
    # 如果表单无效, 返回新建主题的页面
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """在特定主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':  # 确定方法是GET还是POST
        # 只是从服务器读取数据的页面, 使用GET请求
        # 未提交数据: 创建一个新表单(无论是GET还是其他类型的请求, 返回空表单都没问题)
        form = EntryForm()
    else:
        # 在用户需要通过表单提交信息时, 通常使用POST请求
        # POST提交的数据, 对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # 实参commit让Django创建一个新的条目对象, 并将其存储到new_entry中,
            # 而不将它保存到数据库中
            new_entry = form.save(commit=False)
            # 将new_entry的属性topic设置为在这个函数开头从数据库中获取的主题
            new_entry.topic = topic
            check_topic_owner(request, topic)
            # 调用save()将条目保存到数据库中, 并将其与正确的主题相关联
            new_entry.save()
            # 列表args中储存元素topic_id用来衔接到topic后面生成该条目对应主题的URL
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic_id]))
    
    # 如果表单无效, 返回新建主题的页面
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 确认请求的条目所属主题属于当前用户
    check_topic_owner(request, topic)

    if request.method != 'POST':  # 确定方法是GET还是POST
        # 除此请求, 使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # 在用户需要通过表单提交信息时, 通常使用POST请求
        # POST提交的数据, 对数据进行处理
        # 传递实参instance=entry和data=request.POST,
        # 让Django根据既有条目创建一个表单实例,
        # 并根据request.POST中的相关数据对其进行修改
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            # 实参commit让Django创建一个新的条目对象, 并将其存储到new_entry中,
            # 而不将它保存到数据库中
            form.save()
            # 列表args中储存元素topic_id用来衔接到topic后面生成该条目对应主题的URL
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    
    # 如果表单无效, 返回新建主题的页面
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
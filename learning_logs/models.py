from django.db import models
from django.contrib.auth.models import User  # 为了将Topic与User建立外键关系

# Create your models here.
class Topic(models.Model):
    """用户学习的主题"""
    # 由字符或文本组成的数据, 存储少量文本时可以用CharField,
    # 需要告诉Django在数据库中预留多少空间. 这里用来存储主题
    text = models.CharField(max_length=200)
    # 记录日期和时间的数据, 实参auto_now_add=True保证了每当
    # 用户创建新主题时, 都让Django将这个属性自动设置成当前日期和时间
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """返回模型的字符串表示"""
        # 调用方法__str__()来显示模型的简单表示.
        # 这里返回存储在属性text中的字符串
        return self.text

class Entry(models.Model):
    """学到的有关某个主题的具体知识"""
    # 外键, 将每一个新创建的Entry关联到一个父主题Topic
    topic = models.ForeignKey(Topic, None)
    text = models.TextField()  # 不需要长度限制的文本数据类型
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 用来管理模型的额外信息, 让Django在需要使用Entries来表示多个条目,
        # 而不是Entrys
        verbose_name_plural = 'entries'
    
    def __str__(self):
        """返回模型的字符串表示"""
        # 由于条目包含的文本可能很长, 只显示前50个字符
        return self.text[:50] + "..."
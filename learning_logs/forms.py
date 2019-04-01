from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):  # 继承forms.ModelForm
    class Meta:
        model = Topic
        fields = ['text']  # 创建一个表单, 该表单只包含字段text
        labels = {'text': ''}  # 让Django不要为字段text生成标签

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        # 定义属性widgets(小部件-HTML表单元素,
        # 如单行文本框, 多行文本区域或下拉列表)
        # 通过让Django使用forms.Textarea, 定制了字段'text'的输入小部件,
        # 并设置文本区域的宽度为80列, 而不是默认的40列
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
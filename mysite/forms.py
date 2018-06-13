from django import forms
from . import models
from django.contrib.auth.admin import User

class PostForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'}),
                   'password': forms.PasswordInput(attrs={'class': 'form-control'})}


    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '用户名'
        self.fields['password'].label = '密码'

#用户个人信息修改
class PostForm1(forms.ModelForm):
    class Meta:
        model = models.Users
        fields = ['nickname', 'message']
        widgets = {'nickname': forms.TextInput(attrs={'class': 'form-control'}),
                   'message': forms.TextInput(attrs={'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super(PostForm1, self).__init__(*args, **kwargs)
        self.fields['nickname'].label = '昵称'
        self.fields['message'].label = '个人信息'

#登陆，注册
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=15,
                               widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码', max_length=15,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#发文
class PostArticle(forms.ModelForm):
    class Meta:
        model =  models.All_Article
        fields = ['title', 'article']
        widgets = {'title':forms.TextInput(attrs={'class': 'form-control'}),
                   'article':forms.Textarea(attrs={'class':'form-control'})}

    def __init__(self, *args, **kwargs):
        super(PostArticle, self).__init__(*args, **kwargs)
        self.fields['title'].label = '标题'
        self.fields['article'].label = '文章'

#回复
class ReplayForm(forms.ModelForm):
    class Meta:
        model = models.Replay
        fields = ['text']
        widgets = {'text': forms.Textarea( attrs={'class':'form-control','rows':'3',})}

    def __init__(self, *args, **kwargs):
        super(ReplayForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = '回复'

#修改密码
class ChangePSW(forms.Form):
    oldpass = forms.CharField(label='旧密码', max_length=15,
                              widget=forms.PasswordInput(attrs={'class':'form-control'}))
    newpass = forms.CharField(label='新密码', max_length=15,
                              widget=forms.PasswordInput(attrs={'class':'form-control'}))
    checkpass = forms.CharField(label='再次输入', max_length=15,
                              widget=forms.PasswordInput(attrs={'class':'form-control'}))

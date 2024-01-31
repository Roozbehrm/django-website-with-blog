from django import forms
from blog.models import Comment
from captcha.fields import CaptchaField

class CommentForm_public(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Comment
        fields = ['post', 'name', 'email', 'subject', 'message']


class CommentForm_user(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post', 'name', 'email', 'subject', 'message']
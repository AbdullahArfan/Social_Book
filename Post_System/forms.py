from django import forms
from Post_System.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['image', 'caption',]

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = {'text',}
		widgets = {
  			'text': forms.Textarea(attrs={'rows':2, 'cols':1}),
		}

class SignupForm(UserCreationForm):
	email = forms.EmailField(max_length=200, help_text='Required')

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')
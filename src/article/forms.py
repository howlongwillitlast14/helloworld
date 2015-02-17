from django import forms

from .models import Article, Comment

class ArticleForm(forms.ModelForm):
	class Meta:##everything that is not on the form
		model = Article
		fields = ('title', 'body', 'pub_date', 'thumbnail')###To hid likes from the create article template

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'body')
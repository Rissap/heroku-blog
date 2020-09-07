from django import forms

from . import models


class EmailPostForm(forms.Form):
	post_url = forms.CharField(max_length=255)
	name = forms.CharField(max_length=25)
	email = forms.EmailField()
	to = forms.EmailField()
	comment = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
	class Meta:
		model = models.Comment
		fields = ('name', 'email', 'body')
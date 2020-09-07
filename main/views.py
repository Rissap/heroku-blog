from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.core.paginator import PageNotAnInteger

from . import models
from . import forms


# see comments below to explore the 'raw' listview class
class Main(ListView):
	context_object_name = 'posts'
	paginate_by=10
	template_name = 'blog/main.html'

	def get_queryset(self):
		tag = self.request.GET.get("tag")
		if tag:
			return models.Post.published.filter(tags__slug=tag)
		return models.Post.published.all()


class Details(TemplateView):
	template_name = "blog/details.html"

	def get(self, request, year, month, day, post):
		args = {}
		post = get_object_or_404(models.Post,
			status='published',
			slug=post, 
			publish__year=year,
			publish__month=month,
			publish__day=day)

		args["post"] = post
		args["comments"] = post.comments.filter(active=True)
		args["comment_form"] = forms.CommentForm()
		return render(request, self.template_name, args)

	def post(self, request, year, month, day, post):
		args = {}
		post = get_object_or_404(models.Post,
			status='published',
			slug=post, 
			publish__year=year,
			publish__month=month,
			publish__day=day)
		comment = forms.CommentForm(request.POST)
		
		if comment.is_valid():
			comment = comment.save(commit=False)
			comment.post = post
			comment.save()
			args["comment_form"] = forms.CommentForm()
		else:
			args["comment_form"] = forms.CommentForm(request.POST)
		
		args["post"] = post
		args["comments"] = post.comments.filter(active=True)	
		return render(request, self.template_name, args)


class PostShare(TemplateView):
	template_name = "blog/share.html"
	
	def get(self, request, year, month, day, post):
		args = {}

		args["post"] = get_object_or_404(models.Post,
			status='published',
			slug=post, 
			publish__year=year,
			publish__month=month,
			publish__day=day)
		
		return render(request, self.template_name, args)

	def post(self, request, year, month, day, post):
		mail = False
		mail_form = forms.EmailPostForm(request.POST)

		if mail_form.is_valid():
			cleaned = mail_form.cleaned_data
			title = "NoodlesBlog|Message from {0}".format(cleaned["name"])
			body = "Greetings! Comment from {0}:\n\"{1}\".\n\nRead at {2}.\n\nBest withes, NoodlesBlog Team."\
				.format(cleaned["name"], cleaned["comment"], cleaned["post_url"])

			send_mail(title, body, cleaned["email"], [cleaned["to"]])
			mail = True

		args = {"mail": True, "send_mail": mail}
		return render(request, self.template_name, args)


"""
class Main(TemplateView):
	template_name = "blog/main.html"

	def get(self, request):
		args = {}

		post_objects = models.Post.published.all()
		paginator = Paginator(post_objects, 10)
		page = request.GET.get('page')

		try:
			args["posts"] = paginator.page(page)
		except PageNotAnInteger:
			args["posts"] = paginator.page(1)
		except EmptyPage:
			args["posts"] = paginator.page(paginator.num_pages)

		args["page"] = page
		return render(request, self.template_name, args)

	def post(self, request):
		args = {}
		return render("post")
"""
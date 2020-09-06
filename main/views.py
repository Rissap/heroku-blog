from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from . import models


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


class Details(TemplateView):
	template_name = "blog/details.html"

	def get(self, request, year, month, day, post):
		args = {}

		args["post"] = get_object_or_404(models.Post,
			status='published',
			slug=post, 
			publish__year=year,
			publish__month=month,
			publish__day=day)

		return render(request, self.template_name, args)

	def post(self, request):
		args = {}
		return render("post")
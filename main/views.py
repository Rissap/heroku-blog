from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from . import models


class Main(TemplateView):
	template_name = "blog/main.html"

	def get(self, request):
		args = {}
		args["posts"] = models.Post.published.all()

		return render(request, self.template_name, args)

	def post(self, request):
		args = {}
		return render("post")


class Details(TemplateView):
	template_name = "blog/details.html"

	def get(self, request, year, month, day, post):
		args = {}

		args["post"] = get_object_or_404(models.Post,
			slug=post, status='published',
			publish__year=year,
			publish__month=month,
			publish__day=day)

		return render(request, self.template_name, args)

	def post(self, request):
		args = {}
		return render("post")
from django.db.models import Count
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.auth import logout
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from . import models
from . import forms


class Main(ListView):
    model = models.Post
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/main.html'

    def get_queryset(self):
        tag = self.request.GET.get("tag")
        if tag:
            posts =  models.Post.published.filter(tags__slug=tag)
        else:
            posts = models.Post.published.all()

        if not self.request.user.is_authenticated:
            return posts[:10]
        return posts


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

        post_tags = post.tags.values_list('id', flat=True)
        similar = models.Post.published.filter(tags__in=post_tags).exclude(id=post.id)
        args["similars"] = similar.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
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
        
        post_tags = post.tags.values_list('id', flat=True)
        similar = models.Post.published.filter(tags__in=post_tags).exclude(id=post.id)
        args["similars"] = similar.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
        return render(request, self.template_name, args)


class Auth(TemplateView):
    template_name = 'blog/auth.html'


class Login(TemplateView):
    template_name = "blog/auth.html"

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, self.template_name, 
                {"error": True, "text": "Invalid username or password"})

        login(request, user)
        return redirect('/')


class Logout(TemplateView):
    def get(self, request):
        logout(request)
        return redirect("/")


class Register(TemplateView):
    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password1')

        if password != password2:
            return redirect("/auth/")

        user = User.objects.get(username=username)
        if user is None:
            return render(request, self.template_name, 
                    {"error": True, "text": "This user already exists!a"})


        user = authenticate(request, username=username, password=password)
        if user is None:
            user = User.objects.create_user(username, email, password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            login(request, user)
            return redirect("/")
        return render(request, self.template_name, 
                {"error": True, "text": "This user already exists!"})

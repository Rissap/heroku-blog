from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

from . import managers


class Post(models.Model):
	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published')
	)

	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100, unique_for_date='publish')
	author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
	body = models.TextField()
	tags = TaggableManager()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, 
		choices=STATUS_CHOICES, default='draft')

	objects = models.Manager()
	published = managers.PublishedManager()

	class Meta:
		ordering = ('-publish', )

	def get_absolute_url(self):
		return reverse('blog:post_detail',
			args=[self.publish.year, 
			self.publish.strftime('%m'),
			self.publish.strftime('%d'),
			self.slug])

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return 'by {0} on {1}'.format(self.name, self.post)

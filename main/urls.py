from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'main'
urlpatterns = [
	path('', views.Main.as_view(), name='all_posts'),
	path('<int:year>/<int:month>/<int:day>/<str:post>/', views.Details.as_view(),  name='post_detail')
]

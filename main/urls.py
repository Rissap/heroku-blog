from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'main'
urlpatterns = [
	path('', views.Main.as_view(), name='all_posts'),
	path('<int:year>/<int:month>/<int:day>/<str:post>/', views.Details.as_view(),  name='post_detail'),
	path('<int:year>/<int:month>/<int:day>/<str:post>/share/', views.PostShare.as_view(), name="post_share"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

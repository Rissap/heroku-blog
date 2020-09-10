from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'main'
urlpatterns = [
	path('', views.Main.as_view(), name='all_posts'),

	path('auth/', views.Auth.as_view(), name='auth'),
	path('auth/login/', views.Login.as_view(), name="login"),
	path('auth/register/', views.Register.as_view(), name="register"),
	path('auth/logout/', views.Logout.as_view(), name='logout'),

	path('<int:year>/<int:month>/<int:day>/<str:post>/', views.Details.as_view(),  name='post_detail'),
	
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

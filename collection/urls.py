from django.urls import path
from . import views

app_name = 'collection'

urlpatterns = [
	path('', views.collections_render, name='collections'),
	path('get-images', views.ajax_get_images, name='ajax_get_images'),
	path('<str:slug>', views.category_render, name='category'),
	
]
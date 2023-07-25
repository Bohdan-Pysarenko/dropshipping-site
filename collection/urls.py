from django.urls import path
from . import views

app_name = 'collection'

urlpatterns = [
	path('', views.collections_render, name='collections'),
	path('<str:slug>', views.category_render, name='category')
]
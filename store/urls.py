from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('<str:slug>', views.product_render, name='product'),
	path('about/', views.about_us, name='about'),
	path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
	path('shipping_policy/', views.shipping_policy, name='shipping_policy'),
	path('refund_policy/', views.refund_policy, name='refund_policy'),
	path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
]
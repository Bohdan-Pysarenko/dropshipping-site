from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('<str:slug>', views.product_render, name='product'),
	path('cart/', views.cart, name='cart'),
	path('checkout/', views.checkout, name='checkout'),
	path('add-review/', views.add_review, name='add_review'),
	path('add-product/', views.add_product, name='add_product'),
	path('track_order/', views.track_order, name='track_order'),
	path('about/', views.about_us, name='about'),
	path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
	path('shipping-policy/', views.shipping_policy, name='shipping_policy'),
	path('refund-policy/', views.refund_policy, name='refund_policy'),
	path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
	path('subscribe/', views.subscribe, name='subscribe'),
	path('coupon_apply/', views.coupon_apply, name='coupon')
]
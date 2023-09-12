from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('<str:slug>', views.product_render, name='product'),
	path('cart/', views.cart, name='cart'),
	path('checkout/', views.checkout, name='checkout'),
	path('add-review/', views.add_review, name='add_review'),
	path('upload-form-data/', views.upload_form_data, name='upload_form_data'),
	path('add-product/', views.add_product, name='add_product'),
	path('track_order/', views.track_order, name='track_order'),
	path('about/', views.about_us, name='about'),
	path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
	path('shipping-policy/', views.shipping_policy, name='shipping_policy'),
	path('refund-policy/', views.refund_policy, name='refund_policy'),
	path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
	path('contact_us/', views.contact_us, name='contact_us'),
	path('subscribe/', views.subscribe, name='subscribe'),
	path('coupon_apply/', views.coupon_apply, name='coupon'),
	path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
from django.shortcuts import render, get_list_or_404
from .models import *

# Create your views here.
def home(request):
	#planters = Product.objects.all().filter(category=1)
	planters = get_list_or_404(Product, category=1)

	context = {'planters': planters}
	return render(request, 'store/home.html', context)

def product_render(request, slug):
	product = Product.objects.get(slug=slug)
	images = ProductImage.objects.all().filter(product=product)
	attributes = ProductAttribute.objects.all().filter(product=product)
	variants = Variant.objects.all().filter(product=product)
	#print(attributes.value.all())
	context = {'product': product, 'images': images, 'variants': variants}
	return render(request, 'store/product.html', context)

def about_us(request):
	return render(request, 'store/about_us.html')

def shipping_policy(request):
	return render(request, 'store/shipping_policy.html')

def refund_policy(request):
	return render(request, 'store/refund_policy.html')

def privacy_policy(request):
	return render(request, 'store/privacy_policy.html')

def terms_of_service(request):
	return render(request, 'store/terms_of_service.html')

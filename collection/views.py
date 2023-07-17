from django.shortcuts import render
from store.models import *
# Create your views here.

def category_render(request, slug):
	category = Category.objects.get(slug=slug)
	products = category.product_set.all()
	context = {'products': products}
	return render(request, 'collection/category.html', context)

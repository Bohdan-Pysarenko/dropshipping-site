from django.shortcuts import render
from django.http import JsonResponse
from store.models import *
# Create your views here.

def category_render(request, slug):
	category = Category.objects.get(slug=slug)
	products = category.product_set.all()
	context = {'products': products, 'category': category}
	return render(request, 'collection/category.html', context)

def collections_render(request):
	return render(request, 'collection/collections.html')

def ajax_get_images(request):
	review_id = request.GET.get('reviewId', None)
	print("_______________________________________")
	print(review_id)
	review = Review.objects.get(id=review_id)
	images = ReviewImage.objects.filter(review=review)

	image_list = [{'imageURL': image.imageURL} for image in images]

	data = {'images': image_list}
	return JsonResponse(data)
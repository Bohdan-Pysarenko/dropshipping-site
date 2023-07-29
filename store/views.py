from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
def home(request):
	#planters = Product.objects.all().filter(category=1)
	planters = get_list_or_404(Product, category=1)
	categories = Category.objects.all()
	products_list = {}

	for x in range(len(categories)):
		category = categories[x]
		products = category.product_set.all()
		products_list[str(category)] = products


	context = {'planters': planters, 'products_list': products_list}
	return render(request, 'store/home.html', context)

def product_render(request, slug):
	if request.method == 'POST':
		product = Product.objects.get(slug=slug)

		try:
			customer = request.user.customer
		except:
			device = request.COOKIES['device']
			customer, created = Customer.objects.get_or_create(device=device)

		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
		orderItem.quantity=request.POST['quantity']
		orderItem.save()

		return redirect('/cart/')


	product = Product.objects.get(slug=slug)
	images = ProductImage.objects.all().filter(product=product)
	attributes = ProductAttribute.objects.all().filter(product=product)
	variants = Variant.objects.all().filter(product=product)
	reviews = Review.objects.filter(product=product)

	#print(attributes.value.all())
	context = {'product': product, 'images': images, 'variants': variants,
		'reviews': reviews}
	return render(request, 'store/product.html', context)

def cart(request):
	try:
		customer = request.user.customer
	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device=device)

	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	context = {'order':order}
	return render(request, 'store/cart.html', context)

def checkout(request):
	try:
		customer = request.user.customer
	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device=device)

	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	context = {'order':order}
	return render(request, 'store/checkout.html', context)

@login_required
def add_review(request):
	if request.method == 'POST':
		data = request.POST
		images = request.FILES.getlist('images')

		product = Product.objects.get(slug=data['selected_product'])

		review = Review.objects.create(
       		product=product,
			name=data['name'],
			text=data['text'],
			rating=data['rating'],
        )

		for image in images:
			photo = ReviewImage.objects.create(review=review, image=image)

	products = Product.objects.all()
	context = {'products': products}

	return render(request, 'store/add_review.html', context)

@login_required
def add_product(request):
	if request.method == 'POST':
		data = request.POST
		images = request.FILES.getlist('images')

		slug = name_to_slug(data['name'])
		selected_category = data['selected_category']
		selected_category_id = Category.objects.get(slug=selected_category).id

		product = Product.objects.create(
			name=data['name'],
			slug=slug,
			crossed_out_price=data['crossed_out_price'],
			price=data['price'],
			available=data['available'],
			description=data['description']
		)

		for image in images:
			photo = ProductImage.objects.create(product=product, image=image)

		product.category.set([selected_category_id])

	categories = Category.objects.all()
	context = {'categories': categories}
	return render(request, 'store/add_product.html', context)

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


def name_to_slug(name):
	slug = name.lower().replace(' ', '-')
	return slug
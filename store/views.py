from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from .models import *
from .forms import *

# Create your views here.
def handle_404(request, exception):
	return render(request, 'store/404.html', status=404)

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
	try:
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
	except Product.DoesNotExist:
		return redirect('home')

def cart(request):
	try:
		customer = request.user.customer
	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device=device)

	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	coupon_id = request.session.get('coupon_id')
	try:
		coupon = Coupon.objects.get(id=coupon_id, active=True)
		discount = coupon.discount
	except Coupon.DoesNotExist:
		discount = 0

	cart_total = order.get_cart_total * (100 - discount) / 100

	form = CouponApplyForm()

	context = {'order': order, 'cart_total': cart_total, 'form': form}
	return render(request, 'store/cart.html', context)

def checkout(request):
	try:
		customer = request.user.customer
	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device=device)

	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	if request.method == 'POST':
		data = request.POST

		shipping_info = ShippingAddress.objects.create(
			email=data['email'],
			first_name=data['fname'],
			last_name=data['lname'],
			order=order,
			address=data['address'],
			city=data['city'],
			country=data['country'],
			zipcode=data['postal-code']
			)

	context = {'order':order}
	return render(request, 'store/checkout.html', context)

def complete_order(request):
	if request.method == 'POST':
		customer = request.user.customer

		order = Order.objects.get(customer=customer, complete=False)

		order.complete = True
		order.save()

		#order, created = Order.objects.get_or_create(customer=customer, complete=False)
		print(' ')
		print('New order was created for the same customer')
		print(' ')


	return render(request, '')

@login_required
def add_review(request):
	if request.user.is_staff:
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

	else:
		return redirect('home')

@login_required
def add_product(request):
	if request.user.is_staff:
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
	else:
		return redirect('home')

@require_POST
def coupon_apply(request):
	now = timezone.now()
	form = CouponApplyForm(request.POST)
	if form.is_valid():
		code = form.cleaned_data['code']
		print(code)
		try:
			coupon = Coupon.objects.get(code__iexact=code,
				valid_from__lte=now,
				valid_to__gte=now,
				active=True)
			request.session['coupon_id'] = coupon.id
		except Coupon.DoesNotExist:
			request.session['coupon_id'] = None
	return redirect('cart')


def track_order(request):
	return render(request, 'store/track_order.html')

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

def contact_us(request):
	if request.method == 'POST':
		pass
	return render(request, 'store/contact_us.html')

def subscribe(request):
	if request.method == 'POST':
		data = request.POST
		if Subscription.objects.filter(email=data['email']).exists():
			pass
		else:
			subscribtion = Subscription.objects.create(email=data['email'])

			email = EmailMessage(
				'Thank Your For Subscription',
				'There is your discount code',
				settings.EMAIL_HOST_USER,
				[data['email']])

			email.fail_silently=False
			email.send()


	return redirect('home') 

def name_to_slug(name):
	slug = name.lower().replace(' ', '-')
	return slug

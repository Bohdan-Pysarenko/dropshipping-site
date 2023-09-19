from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from .models import *
from .forms import *
import json
from time import sleep

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

def product_render(request, slug, variant_title=None, variant_price=None):
	try:
		if request.method == 'POST':
			data = json.loads(request.body)
			
			variant_title = data[1]
			variant_price = float(data[2])
			
			

			try:
				customer = request.user.customer
			except:
				device = request.COOKIES['device']
				customer, created = Customer.objects.get_or_create(device=device)

			order, created = Order.objects.get_or_create(customer=customer, complete=False)
			if variant_title == None and variant_price == None:
				product = Product.objects.get(slug=slug)
				orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
				orderItem.quantity=request.POST['quantity']
				orderItem.save()
			else:
				product = Product.objects.get(slug=slug)
				slug = data[0]
				quantity = int(data[3])
				orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, variant_title=variant_title, variant_price=variant_price)
				print('Order Item: ', orderItem, orderItem.id)
				orderItem.quantity=quantity
				orderItem.save()

			return redirect('/cart/')


		product = Product.objects.get(slug=slug)
		images = ProductImage.objects.all().filter(product=product)

		product_attributes = ProductAttribute.objects.filter(product=product)
		unique_attributes = ProductAttribute.objects.filter(product=product).values_list('attribute__attribute__name', flat=True).distinct()
		attribute_value_map = {}

		for attribute_name in unique_attributes:
		    attribute_values = ProductAttribute.objects.filter(product=product, attribute__attribute__name=attribute_name).values_list('attribute__value', flat=True).distinct()
		    attribute_value_map[attribute_name] = list(attribute_values)


		reviews = Review.objects.filter(product=product)


		context = {'product': product, 'images': images, 'attribute_value_map': attribute_value_map,
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
	orderItems = order.orderitem_set.all()

	coupon_id = request.session.get('coupon_id')
	try:
		coupon = Coupon.objects.get(id=coupon_id, active=True)
		discount = coupon.discount
	except Coupon.DoesNotExist:
		discount = 0

	cart_total = order.get_cart_total * (100 - discount) / 100

	form = CouponApplyForm()

	context = {'order': order, 'orderItems': orderItems, 'cart_total': cart_total, 'form': form}
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
			data = json.loads(request.body)

			slug = data[0]
			product = Product.objects.get(slug=slug)

			attributes_list = []
			for x in range(len(data[1])):
				attribute_name = data[1][x]
				attribute, _ = Attribute.objects.get_or_create(name=attribute_name)
				attributes_list.append(attribute)

			for x in range(2, len(data)):
				combination = data[x] #{'variant': ['White', 's'], 'price': '15'}

				product_attribute = ProductAttribute.objects.create(product=product, price_modifier=combination['price'])

				for y in range(len(combination['variant'])):
					attribute_value, _ = AttributeValue.objects.get_or_create(attribute=attributes_list[y], value=combination['variant'][y])
					product_attribute.attribute.add(attribute_value)


				print(product_attribute.attribute.all())

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

@require_POST
def upload_form_data(request):
	if request.method == 'POST':
		data = request.POST

		images = request.FILES.getlist('images')

		slug = name_to_slug(data['name'])
		selected_category = data['selected_category']
		selected_category_id = Category.objects.get(slug=selected_category).id

		try:
			available = data['available']
		except:
			available = False
		product = Product.objects.create(
			name=data['name'],
			slug=slug,
			crossed_out_price=data['crossed_out_price'],
			price=data['price'],
			available=available,
			description=data['description']
		)

		for image in images:
			photo = ProductImage.objects.create(product=product, image=image)

		product.category.set([selected_category_id])
        

		return JsonResponse({'slug': slug})
	return JsonResponse({'error': 'No form data were sent.'}, status=400)

@require_POST
def variant_price(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		print(data)
		slug = data[0]
		product = Product.objects.get(slug=slug)

		product_attributes = ProductAttribute.objects.filter(product=product)
		desired_attributes = data[1:]
		modifier = None

		for product_attribute in product_attributes:
		    attribute_values = product_attribute.attribute.all()
		    attribute_values_list = [attribute_value.value for attribute_value in attribute_values]

		    if set(desired_attributes) == set(attribute_values_list):
		        modifier = product_attribute.price_modifier
		        print(modifier)
		        break
		
		response_data = {'modifier': modifier}

		return JsonResponse(response_data)
@require_POST
def update_quantity(request):
	data = json.loads(request.body) # [order_id, product_name, variants_name, new_quantity]

	order = Order.objects.get(id=int(data[0]))
	product = Product.objects.get(name=data[1])

	order_item = OrderItem.objects.get(order=order, product=product, variant_title=data[2])
	# print(order_item)
	order_item.quantity = data[3]
	order_item.save()

	return JsonResponse({})

@require_POST
def remove_order_item(request):
	data = json.loads(request.body) # [order_id, product_name, variants_name]

	order = Order.objects.get(id=int(data[0]))
	product = Product.objects.get(name=data[1])

	order_item = OrderItem.objects.get(order=order, product=product, variant_title=data[2])
	order_item.delete()
	return JsonResponse({})

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




















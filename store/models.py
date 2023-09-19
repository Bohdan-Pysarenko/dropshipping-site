from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import os
from decimal import Decimal

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	device = models.CharField(max_length=200, null=True)

	# def __str__(self):
	# 	return self.name


####################################

class Category(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True, blank=True)

	def __str__(self):
		return self.name

class Attribute(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class AttributeValue(models.Model):
	attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
	value = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.attribute} ({self.value})'

class Product(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	category = models.ManyToManyField(Category)
	image = models.ImageField(null=True, blank=True)
	crossed_out_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	available = models.BooleanField(default=True,null=True, blank=True)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name

	def calc_save(self):
		save_persent = (self.crossed_out_price - self.price) / self.crossed_out_price * 100
		return round(save_persent)

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

	@property
	def first_image_url(self):
		try:
			# Отримати перший об'єкт ProductImage, якщо вони є
			first_image = self.productimage_set.first()
			if first_image:
				return first_image.image.url
			else:
				return ''  # Повернути порожній рядок, якщо зображень немає
		except:
			return ''

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ManyToManyField(AttributeValue, blank=True)
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    crossed_out_price_modified = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.product.name} - {self.attribute.all()} (Modifier: {self.price_modifier})'

    def get_attribute_value(self):
    	return self.attribute.value


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return f'{self.product.name} - Image'

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url


class Review(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
	name = models.CharField(max_length=255, null=True)
	text = models.TextField()
	rating = models.IntegerField()

	def __str__(self):
		return f'Review for {self.product.name}'

	def get_average_rating(self):
		reviews_for_product = Review.objects.filter(product=self.product)

		total_rating_sum = sum(review.rating for review in reviews_for_product)

		if reviews_for_product:
			average_rating = total_rating_sum / len(reviews_for_product)
		else:
			average_rating = 5

		return average_rating

class ReviewImage(models.Model):
	review = models.ForeignKey(Review, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='images/review_photos/', null=True, blank=True)

	def __str__(self):
		return f'{self.review.product.name} - Image'

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=False)
	transaction_id = models.CharField(max_length=200, null=True)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])

		return float(total) 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	variant_title = models.CharField(max_length=500, null=True, blank=True)
	variant_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		if self.variant_price == None:
			total = self.product.price * self.quantity
		else:
			total = self.variant_price * self.quantity
		return total

class Coupon(models.Model):
	code = models.CharField(max_length=50, unique=True)
	valid_from = models.DateTimeField()
	valid_to = models.DateTimeField()
	discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.code

class ShippingAddress(models.Model):
	email = models.EmailField()
	first_name = models.CharField(max_length=200, null=True)
	last_name = models.CharField(max_length=200, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	country = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	# def __str__(self):
	# 	return str(self.email) if self.email else "No Email Provided"

class Subscription(models.Model):
	email = models.EmailField()

	def __str__(self):
		return str(self.email)

class ContactUs(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField()
	message = models.TextField()


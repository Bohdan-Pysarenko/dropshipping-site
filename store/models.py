from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	device = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name


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

	attributes = models.ManyToManyField(AttributeValue, through='ProductAttribute')

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

class Variant(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	color = models.CharField(max_length=100, null=True, blank=True)
	size = models.CharField(max_length=100, null=True, blank=True)
	material = models.CharField(max_length=100, null=True, blank=True)
	power = models.CharField(max_length=100, null=True, blank=True)
	number_in_group = models.CharField(max_length=100, null=True, blank=True)
	crossed_out_price = models.DecimalField(max_digits=8, decimal_places=2)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	available = models.BooleanField(default=True, blank=True)

	def __str__(self):
		return f'{self.product.name} - {self.color} - {self.size} - {self.material} - {self.power} - {self.number_in_group}'

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2)
    crossed_out_price_modified = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} - {self.attribute.value} (Modifier: {self.price_modifier})'


# class ProductAttribute(models.Model):
# 	product = models.ForeignKey(Product, on_delete=models.CASCADE)
# 	attribute = models.ManyToManyField(Attribute, blank=True)
# 	value = models.ManyToManyField(AttributeValue, blank=True)
# 	crossed_out_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
# 	price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
# 	available = models.BooleanField(default=True, blank=True)

# 	def __str__(self):
# 		return f'{self.product.name} - {self.value}'


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
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	name = models.CharField(max_length=255, null=True)
	text = models.TextField()
	rating = models.IntegerField()

	def __str__(self):
		return f'Review for {self.product.name}'

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

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	email = models.EmailField() 
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	country = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address

"""
class Product(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
"""


"""
def get_upload_path(instance, filename):
    return os.path.join(instance.product.name, filename)
"""
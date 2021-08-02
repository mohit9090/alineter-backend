from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

def productpic_directory_path(instance, filename):
	ext = filename.split('.')[1]
	product_name = instance.product_name.strip().replace(' ', '-')
	filename = f'{product_name}-{instance.id}.{ext}'
	
	return f'alineter/product/{filename}'


class TestProduct(models.Model):
	product_name = models.CharField(max_length=255, default='This is name of Product')
	product_img = models.ImageField(upload_to=productpic_directory_path)
	product_price = models.FloatField()
	product_discount = models.FloatField(default=20)
	product_sellprice = models.FloatField(null=True, blank=True)

	def __str__(self):
		return self.product_name

	def save(self, *args, **kwargs):
		price_diff = self.product_price * self.product_discount
		self.product_sellprice = self.product_price - price_diff/100
		super(TestProduct, self).save(*args, **kwargs)



class TestProductQuantity(models.Model):
	product = models.OneToOneField(TestProduct, on_delete=models.CASCADE)
	avail_quantity = models.IntegerField()

	def __str__(self):
		return f'{self.product}, stock={self.avail_quantity}'

	class Meta:
		verbose_name_plural = 'Test Product Quantities'



class ProductCart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(TestProduct, on_delete=models.CASCADE)
	# date_add = models.DateTimeField(auto_now_add=True)
	# date_updated = models.DateTimeField(auto_now=True)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return f'{self.user} - {self.product}' 

	class Meta:
		verbose_name_plural = 'Product cart'
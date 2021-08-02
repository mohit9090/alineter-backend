from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# def productpic_directory_path(instance, filename):
# 	ext = filename.split('.')[1]
# 	product_name = instance.product_name.strip().replace(' ', '-')
# 	filename = f'{product_name}-{instance.id}'
# 	return filename


# class TestProduct(models.Model):
# 	product_name = models.CharField(max_length=255, default='This is name of Product')
# 	product_img = models.ImageField(upload_to=productpic_directory_path)
# 	product_price = models.DecimalField(decimal_places=2)
# 	product_discount = models.DecimalField(decimal_places=2, default=20)
# 	product_sellprice = models.DecimalField(decimal_places=2)
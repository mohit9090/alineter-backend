from django.db import models
import uuid

# from django.contrib.auth.models import User, Group
# from django.contrib.auth.hashers import make_password

# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from PIL import Image


# class Customer(models.Model):
# 	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	mobile = models.CharField(max_length=10, null=False, blank=False)
# 	city = models.CharField(max_length=80, null=False, blank=False)
# 	street = models.TextField(null=False, blank=False)
# 	pincode = models.CharField(max_length=6, null=False, blank=False)
# 	state = models.CharField(max_length=50, null=False, blank=False)
# 	country = models.CharField(max_length=30, null=False, blank=False)
# 	profile_pic = models.ImageField(upload_to='customer/pfpic', null=True, blank=True)

# 	def __str__(self):
# 		return self.user.username


# 	def get_address(self):
# 		return f'{self.street}, {self.city}, PIN-{self.pincode}, {self.state}, {self.country}'



# # Create an user instance in Customer Profile
# @receiver(post_save, sender=User)
# def link_customer_profile(sender, instance, created, **kwargs):
# 	if created:
# 		Customer.objects.create(user=instance)


# # Update user instance in Customer Profile
# @receiver(post_save, sender=User)
# def update_customer_profile(sender, instance, created, **kwargs):
# 	if not(created):
# 		instance.customer.save()



# https://stackoverflow.com/questions/15140942/django-imagefield-change-file-name-on-upload

	





# in settings.py
# AUTH_USER_MODEL = 'auth_page.Account'
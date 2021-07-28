from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver
User = get_user_model()

# 3rd party import
from PIL import Image


def profilepic_directory_path(instance, filename):
	"""
	Change filename of profile picture
	"""
	ext = filename.split('.')[1]
	filename = f'{instance.user.username}-pic.${ext}'

	return f'customer/profilepic/{filename}' 


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	mobile = models.CharField(verbose_name='Mobile Number', max_length=10)
	landmark = models.TextField(verbose_name='Landmark', null=True, blank=True)
	street_address = models.TextField(verbose_name='Street Address')
	city = models.CharField(verbose_name='City', max_length=40)
	pin = models.CharField(verbose_name='PIN', max_length=6)
	state = models.CharField(verbose_name='State', max_length=30)
	country = models.CharField(verbose_name='Country', max_length=30)
	profile_pic = models.ImageField(upload_to=profilepic_directory_path, verbose_name='Profile Pic', blank=True, null=True)

	def __str__(self):
		return self.user.username

	def get_address(self):
		return f"{self.landmark if self.landmark else ''}\n{self.street_address},\n{self.city}, Pin-{self.pin},\n{self.state}, {self.country}"

	def save(self, *args, **kwargs):
		if self.state and self.country:
			self.state = self.state.capitalize()
			self.country = self.country.capitalize()

		if self.profile_pic:
			super(Customer, self).save(*args, **kwargs)
			img = Image.open(self.profile_pic.path)
			if img.height>200 and img.width>200:
				set_dim = (200, 200)
				img.thumbnail(set_dim)
			img.save(self.profile_pic.path, quality=50)

		super(Customer, self).save(*args, **kwargs)




"""
Link User model to Customer model on creation of user instance
"""
@receiver(post_save, sender=User)
def createCustomer(sender, instance, created, **kwargs):
	try:
		customer_group = Group.objects.get(name='customer')
	except Group.DoesNotExist:
		pass
	else: 
		instance.groups.add(customer_group) # Add this user to customer group

	if created:
		Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def updateCustomer(sender, instance, created, **kwargs):
	if not created:
		instance.customer.save()



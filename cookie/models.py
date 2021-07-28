from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
User = get_user_model() 


class Cookie(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	cookie_id = models.CharField(max_length=255)
	creation_date = models.DateTimeField(auto_now_add=True)
	expiry_date = models.DateTimeField()

	def __str__(self):
		return self.cookie_id



""" Delete the previous instance of user if it is already existing """
@receiver(pre_save, sender=Cookie)
def check_existence(sender, instance, **kwargs):
	try:
		prev_user_instance = Cookie.objects.get(user=instance.user)
	except Cookie.DoesNotExist:
		return
	else:
		prev_user_instance.delete()



# 2021-07-27 14:26:35.992036+00:00  ----  2021-07-27 14:27:36.472036+00:00  ----  2021-07-27 20:01:40.436411
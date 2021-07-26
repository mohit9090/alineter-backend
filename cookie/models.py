from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model() 


class Cookie(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	cookie_id = models.CharField(max_length=255)
	creation_date = models.DateTimeField(auto_now_add=True)
	expiry_date = models.DateTimeField()

	def __str__(self):
		return self.cookie_id


""" 

if the cookie with the user already exists by chanace then delete the previous cookie

"""
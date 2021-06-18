from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()



class CompanyReview(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	review = models.TextField(verbose_name='Review')
	rating = models.PositiveIntegerField(verbose_name='Rating')
	date_reviewed = models.DateTimeField(verbose_name='Review Date', auto_now_add=True)

	def __str__(self):
		return f'{self.user.username} rated {self.rating} star'
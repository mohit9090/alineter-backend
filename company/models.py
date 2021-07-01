from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()



class CompanyReview(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	review = models.TextField(verbose_name='Review')
	rating = models.PositiveIntegerField(verbose_name='Rating')
	date_reviewed = models.DateTimeField(verbose_name='Review Date', auto_now_add=True)
	highlight = models.BooleanField(verbose_name='Highlight this Review', default=False)

	def __str__(self):
		return f'{self.user.username} rated {self.rating} star'

	def save(self, *args, **kwargs):
		if self.rating <= 0:
			self.rating = 0
		elif self.rating > 5:
			self.rating = 5
		super(CompanyReview, self).save(*args, **kwargs) 
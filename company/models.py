from django.db import models
from django.utils.timesince import timesince

from django.contrib.auth import get_user_model
User = get_user_model()

from PIL import Image


def profilepic_directory_path(instance, filename):
	ext = filename.split('.')[1]
	username = ''.join(instance.name.split(' '))
	filename = f'{username}.${ext}'

	return f'alineter/founder/{filename}'


class Company(models.Model):
	name = models.CharField(verbose_name='Company Name', max_length=15)
	tag = models.CharField(verbose_name='Company Tag', max_length=255)
	active = models.BooleanField(verbose_name='Company Status', default=True)
	website = models.URLField(verbose_name='Company Website', max_length=50)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Company'


class CompanyInfo(models.Model):
	MODES = (
		('public', 'Public'),
		('private', 'Private'),
		('joint', 'Joint')
	)
	company = models.OneToOneField(Company, on_delete=models.CASCADE)
	full_name = models.CharField(verbose_name='Company Fullname', max_length=100)
	cin = models.CharField(verbose_name='CIN', max_length=100)
	registration_number = models.CharField(verbose_name='Registration Number', max_length=20)
	founded = models.DateTimeField(verbose_name='Founded In')
	mode = models.CharField(verbose_name='Company Mode', choices=MODES, max_length=20)
	company_category = models.CharField(verbose_name='Company Category', max_length=100)
	company_subcategory = models.CharField(verbose_name='Company Subcategory', max_length=100)
	company_activity = models.TextField(verbose_name='Company Activity')
	members = models.IntegerField(verbose_name='Company Members', default=2)

	def __str__(self):
		return self.full_name

	def get_age(self):
		return timesince(self.founded)

	class Meta:
		verbose_name_plural = 'Company info'


class CompanyAddress(models.Model):
	company = models.OneToOneField(Company, on_delete=models.CASCADE)
	street = models.TextField(verbose_name='Street Address')
	city = models.CharField(verbose_name='City', max_length=40)
	pin = models.CharField(verbose_name='PIN', max_length=6)
	district = models.CharField(verbose_name='District', max_length=30)
	state = models.CharField(verbose_name='State', max_length=30)
	country = models.CharField(verbose_name='Country', max_length=30)

	def get_address(self):
		return f'{self.street}, {self.city}, {self.district}, {self.state}, {self.country} - {self.pin}'

	def __str__(self):
		return self.get_address()

	def save(self, *args, **kwargs):
		if self.state and self.country:
			self.state = self.state.capitalize()
			self.country = self.country.capitalize()
		super(CompanyAddress, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = 'Company address'


class CompanyEmailHelpline(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	helpline = models.CharField(verbose_name='Helpline Type', max_length=20)
	email = models.EmailField(verbose_name='Email')

	def __str__(self):
		return f'{self.helpline} - {self.email}'

	class Meta:
		verbose_name_plural = 'Company email helpline'


class CompanyTelephoneHelpline(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	helpline = models.CharField(verbose_name='Helpline Type', max_length=20)
	telephone = models.CharField(verbose_name='Telephone', max_length=15)

	def __str__(self):
		return f'{self.helpline} - {self.telephone}'

	class Meta:
		verbose_name_plural = 'Company telephone helpline'


class CompanyFounder(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	name = models.CharField(verbose_name='Name', max_length=50)
	email = models.EmailField(verbose_name='Email')
	designation = models.CharField(verbose_name='Designation', max_length=30)
	profile_pic = models.ImageField(upload_to=profilepic_directory_path, verbose_name='Profile Pic')
	bio = models.TextField(verbose_name='About Founder')

	def __str__(self):
		return f'{self.name}, {self.designation}'


	def save(self, *args, **kwargs):
		if self.profile_pic:
			super(CompanyFounder, self).save(*args, **kwargs)
			img = Image.open(self.profile_pic.path)
			if img.height > 500 and img.width > 500:
				dim = (500, 500)
				img.thumbnail(dim)
			img.save(self.profile_pic.path, quality=100)
		super(CompanyFounder, self).save(*args, **kwargs)


class CustomerQuery(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	name = models.CharField(verbose_name='Customer Name', max_length=60)
	email = models.EmailField(verbose_name='Email')
	date_posted = models.DateTimeField(auto_now_add=True)
	subject = models.CharField(verbose_name='Subject', max_length=255)
	content = models.TextField(verbose_name='Content')

	def __str__(self):
		return f'{self.email} - {self.subject}'

	class Meta:
		verbose_name_plural = 'Customer query'


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
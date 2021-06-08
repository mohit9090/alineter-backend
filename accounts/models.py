from django.db import models
from django.contrib.auth.models import Group, AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
import re


class UserManager(BaseUserManager):
	def create_user(self, email, first_name, password=None):
		"""
		Creates and save a User
		"""
		if not email:
			raise ValueError('Users must have an Email address')
		
		if not first_name:
			raise ValueError('Users must have a First name')

		user = self.model(
			email=self.normalize_email(email),
			first_name=first_name
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_staffuser(self, email, first_name, password):
		"""
		Creates and save a Staff User
		"""
		if not email:
			raise ValueError('Staff Users must have an Email address')
		
		if not first_name:
			raise ValueError('Staff Users must have a First name')

		user = self.create_user(
			email=self.normalize_email(email),
			first_name=first_name
		)

		user.set_password(password)
		user.is_staff = True
		user.save(using=self._db)
		return user

	def create_superuser(self, email, first_name, password):
		"""
		Creates and save a Superuser
		"""
		if not email:
			raise ValueError('Users must have an Email address')
		
		if not first_name:
			raise ValueError('Users must have an First name')

		user = self.create_user(
				email=self.normalize_email(email),
				first_name=first_name
			)
		user.set_password(password)
		user.is_superuser=True
		user.is_admin=True
		user.is_staff=True
		user.save(using=self._db)
		return user



class User(AbstractBaseUser):
	id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
	email = models.EmailField(verbose_name='Email address', max_length=60, unique=True)
	username = models.CharField(verbose_name='Username', max_length=50, blank=True, null=True)

	first_name = models.CharField(verbose_name='First name', max_length=30)
	last_name = models.CharField(verbose_name='Last name', max_length=30)
	
	date_joined = models.DateTimeField(verbose_name='Date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='Last login', auto_now=True)
	
	is_admin = models.BooleanField(verbose_name='Admin', default=False)
	is_superuser = models.BooleanField(verbose_name='Superuser', default=False)
	is_active = models.BooleanField(verbose_name='Active user', default=True)
	is_staff = models.BooleanField(verbose_name='Staff', default=False)
	
	groups = models.ManyToManyField(Group)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'password']

	objects = UserManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True 

	def get_full_name(self):
		return f'{self.first_name} {self.last_name if self.last_name else ""}'

	def get_short_name(self):
		return f'{self.first_name}'

	def save(self, *args, **kwargs):
		if not self.username:
			extracted_name = self.email.split('@')[0]
			formatted_name = re.sub('[#$%&*+=?^`{|}~-]', '' , extracted_name)
			
			if len(User.objects.filter(username__iexact=formatted_name)):
				# username already exists
				import random
				self.username = f'{formatted_name}{random.randint(1111, 9999)}'
			else:
				self.username = formatted_name
		super(User, self).save(*args, **kwargs)



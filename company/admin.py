from django.contrib import admin

from . models import CompanyReview


class CompanyReviewAdmin(admin.ModelAdmin):
	readonly_fields = ('date_reviewed',)

	list_display = ['user', 'rating', 'highlight']
	list_filter = ['rating', 'date_reviewed', 'highlight']

	ordering = ['-date_reviewed']



admin.site.register(CompanyReview, CompanyReviewAdmin) 
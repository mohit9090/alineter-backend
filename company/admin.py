from django.contrib import admin

from . models import CompanyReview


class CompanyReviewAdmin(admin.ModelAdmin):
	readonly_fields = ('date_reviewed',)

	list_display = ['user', 'rating']
	list_filter = ['rating', 'date_reviewed']

	ordering = ['-date_reviewed']



admin.site.register(CompanyReview, CompanyReviewAdmin) 
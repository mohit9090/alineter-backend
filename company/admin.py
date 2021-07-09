from django.contrib import admin

from . models import (Company, CompanyInfo, CompanyAddress, 
	CompanyEmailHelpline, CompanyTelephoneHelpline, 
	CompanyFounder, CustomerQuery, CompanyFaq ,CompanyReview,
	CompanyTermsCondition, CompanyPrivacyPolicy)

class CompanyAdmin(admin.ModelAdmin):
	list_display = ['name', 'website', 'active']


class CompanyInfoAdmin(admin.ModelAdmin):
	list_display = ['full_name', 'mode', 'founded', 'members']


class CompanyAddressAdmin(admin.ModelAdmin):
	list_display = ['street', 'city', 'pin', 'state']
	fieldsets = (
		('Address', {'fields': ('company', 'street', 'city', 'pin', 'district', 'state', 'country',)}),
	)


class CompanyEmailHelplineAdmin(admin.ModelAdmin):
	list_display = ['helpline', 'email']
	list_filter = ['helpline']


class CompanyTelephoneHelplineAdmin(admin.ModelAdmin):
	list_display = ['helpline', 'telephone']
	list_filter = ['helpline']


class CompanyFounderAdmin(admin.ModelAdmin):
	list_display = ['name', 'designation', 'email']


class CustomerQueryAdmin(admin.ModelAdmin):
	readonly_fields = ('date_posted',)
	list_display = ['email', 'subject', 'date_posted']
	list_filter = ['date_posted']

	ordering = ['-date_posted']


class CompanyReviewAdmin(admin.ModelAdmin):
	readonly_fields = ('date_reviewed',)

	list_display = ['user', 'rating', 'highlight']
	list_filter = ['rating', 'date_reviewed', 'highlight']

	ordering = ['-date_reviewed']


class CompanyFaqAdmin(admin.ModelAdmin):
	list_display = ['question', 'asked_date']
	list_filter = ['asked_date']

	ordering = ['-asked_date']


class CompanyTermsConditionPrivacyPolicyAdmin(admin.ModelAdmin):
	list_display = ['date_modified', 'date_created']





 
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyAddress, CompanyAddressAdmin)
admin.site.register(CompanyEmailHelpline, CompanyEmailHelplineAdmin)
admin.site.register(CompanyTelephoneHelpline, CompanyTelephoneHelplineAdmin)
admin.site.register(CompanyFounder, CompanyFounderAdmin)
admin.site.register(CompanyReview, CompanyReviewAdmin)
admin.site.register(CompanyInfo, CompanyInfoAdmin)
admin.site.register(CustomerQuery, CustomerQueryAdmin)
admin.site.register(CompanyFaq, CompanyFaqAdmin)
admin.site.register(CompanyTermsCondition, CompanyTermsConditionPrivacyPolicyAdmin)
admin.site.register(CompanyPrivacyPolicy, CompanyTermsConditionPrivacyPolicyAdmin)
from django.contrib import admin

from .models import Employee, Company, Review, Request

admin.site.register(Employee)
admin.site.register(Company)
admin.site.register(Review)
admin.site.register(Request)

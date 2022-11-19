from django.contrib import admin
from .models import *

class BenefitsAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'amount', 'title', 'time_stamp', 'sender']

admin.site.register(Benefits, BenefitsAdmin)

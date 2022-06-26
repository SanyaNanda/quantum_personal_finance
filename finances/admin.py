from django.contrib import admin
from .models import *

class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'amount', 'source', 'note', 'time_stamp', 'category']

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'amount', 'expense', 'note', 'time_stamp', 'category']

class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'name', 'total_amount']

class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'name', 'total_amount']

admin.site.register(Income, IncomeAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(IncomeCategory, IncomeCategoryAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)

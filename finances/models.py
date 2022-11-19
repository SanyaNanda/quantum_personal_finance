from django.db import models
from django.contrib.auth.models import User

# from django.utils import timezone

class ExpenseCategory(models.Model):
    profile = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='expense_categoty_user')
    name = models.CharField(max_length=250, blank=False)
    total_amount = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name

class IncomeCategory(models.Model):
    profile = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='income_category_user')
    name = models.CharField(max_length=250, blank=False)
    total_amount = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Income(models.Model):
    profile = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='income_user')
    time_stamp = models.DateField()
    source = models.CharField(max_length=250, blank=False)
    amount = models.FloatField()
    note = models.CharField(max_length=5000, blank=True)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, related_name='income_category')
    
    def __str__(self):
        return self.source

class Expense(models.Model):
    profile = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='expense_user')
    time_stamp = models.DateField()
    expense = models.CharField(max_length=250, blank=False)
    amount = models.IntegerField()
    note = models.CharField(max_length=5000, blank=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='expense_category')

    def __str__(self):
        return self.expense
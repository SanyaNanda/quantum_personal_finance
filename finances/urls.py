# from turtle import home
from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'financeS'

urlpatterns = [
   path('home/<username>/', DashboardView,name="home"),
   path('add-income/<username>/', AddIncomeView,name="add-income"),
   path('update-income/<username>/<int:id>', UpdateIncomeView,name="update-income"),
   path('delete-income/<username>/<int:id>', DeleteIncomeView,name="delete-income"),
   path('add-expense/<username>/', AddExpenseView,name="add-expense"),
   path('update-expense/<username>/<int:id>', UpdateExpenseView,name="update-expense"),
   path('delete-expense/<username>/<int:id>', DeleteExpenseView,name="delete-expense"),
   path('add-income-category/<username>/', AddIncomeCategoryView,name="add-income-category"),
   path('add-expense-category/<username>/', AddExpenseCategoryView,name="add-expense-category"),
   path('dashboard/<username>/', DashboardView,name="dashboard"),
   path('expense/<username>/', ExpenseView,name="expense"),
   path('income/<username>/', IncomeView,name="income"),

]
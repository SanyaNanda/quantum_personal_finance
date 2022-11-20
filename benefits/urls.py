# from turtle import home
from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'benefits'

urlpatterns = [
   path('home/<username>/', BenefitsView,name="benefit-add-n-list"),
   path('update-benefit/<username>/<int:id>', UpdateBenefitsView,name="update-benefit"),
   path('delete-benefit/<username>/<int:id>', DeleteBenefitsView,name="delete-benefit")

]
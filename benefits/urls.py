# from turtle import home
from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'benefits'

urlpatterns = [
   path('home/<username>/', BenefitsView,name="benefit-add-n-list"),
   path('home/<username>/<int:id>', UpdateBenefitsView,name="update-benefit"),
   path('home/<username>/<int:id>', DeleteBenefitsView,name="delete-benefit")

]
from django.urls import path
from . import views

app_name = "authenticate"   

urlpatterns = [
    path("", views.Home, name="home"),
    path("signup/", views.SignUpView,name="signup"),
    path("login/", views.LoginView,name="login"),
    path("logout/", views.LogoutView, name="logout"),
]
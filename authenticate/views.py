from django.shortcuts import render

# Create your views here.
from django.shortcuts import  redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User


####################################################################

# Home page
def Home(request):
    return render(request,"home.html")

####################################################################

# Sign up
def SignUpView(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        # age = request.POST['age']
        # gender = request.POST['gender']
        password1 = request.POST['password']
        password2 = request.POST['cpassword']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'rr.html', {'message': 'Email already registered.'})
            user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name,last_name=last_name)
            user.save()
            # doctor = DoctorProfile(user=user)
            # doctor.age = age
            # doctor.save()
            return redirect('authenticate:login')
    return render(request = request, template_name = 'register.html',)

####################################################################

# Login
def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('finances:home', username=username)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request = request, template_name = "login.html",)

####################################################################

# Logout
def LogoutView(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("authenticate:home")

####################################################################


from django.shortcuts import render
from django.shortcuts import  redirect
from django.contrib.auth.models import User
from .models import Income, Expense, IncomeCategory, ExpenseCategory

####################################################################

# Home page
def HomeView(request, username=None):
    return render(request,"finances/home.html")

####################################################################

def AddIncomeView(request, username=None):
    profile = User.objects.get(username=username)
    category = IncomeCategory.objects.filter(profile__username=username)
    if request.method == 'POST':
        time_stamp = request.POST['time_stamp']
        source = request.POST['source']
        amount = request.POST['amount']
        note = request.POST['note']
        category = IncomeCategory.objects.get(id=request.POST.get('category'))
        income = Income(profile=profile,source=source,amount=amount,note=note, time_stamp=time_stamp, category=category)
        income.save()
        return redirect('finances:home', username=username)
    template = 'finances/add_income.html'
    context = {
        'category_list':category,
    }
    return render(request, template, context)

####################################################################

def AddExpenseView(request, username=None):
    profile = User.objects.get(username=username)
    category = ExpenseCategory.objects.filter(profile__username=username)
    if request.method == 'POST':
        time_stamp = request.POST['time_stamp']
        expense = request.POST['expense']
        amount = request.POST['amount']
        note = request.POST['note']
        category = ExpenseCategory.objects.get(id=request.POST.get('category'))
        expense = Expense(profile=profile,expense=expense,amount=amount,note=note, time_stamp=time_stamp, category=category)
        expense.save()
        return redirect('finances:home', username=username)
    template = 'finances/add_expense.html'
    context = {
        'category_list':category,
    }
    return render(request, template, context)


####################################################################

def AddExpenseCategoryView(request, username=None):
    profile = User.objects.get(username=username)
    if request.method == 'POST':
        name = request.POST['name']
        expense = ExpenseCategory(profile=profile,name=name)
        expense.save()
        return redirect('finances:home', username=username)
    template = 'finances/add_expense_category.html'
    return render(request, template)

####################################################################

def AddIncomeCategoryView(request, username=None):
    profile = User.objects.get(username=username)
    if request.method == 'POST':
        name = request.POST['name']
        income = IncomeCategory(profile=profile,name=name)
        income.save()
        return redirect('finances:home', username=username)
    template = 'finances/add_income_category.html'
    return render(request, template)



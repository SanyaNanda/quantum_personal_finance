from calendar import month
from django.shortcuts import render
from django.shortcuts import  redirect
from django.contrib.auth.models import User
from .models import Income, Expense, IncomeCategory, ExpenseCategory
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Sum

####################################################################

# Home page
@login_required
def HomeView(request, username=None):
    profile = User.objects.get(username=username)
    context = {
        'profile':profile,
    }
    return render(request,"finances/home.html",context)

####################################################################

def AddIncomeView(request, username=None):
    profile = User.objects.get(username=username)
    category = IncomeCategory.objects.filter(profile__username=username)
    # print(category)
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

####################################################################

def DashboardView(request, username=None):
    profile = User.objects.get(username=username)
    today = datetime.date.today()
    # month = today.month-1
    # year = today.year
    if 'month' in request.GET and 'year' in request.GET:
        month = request.GET['month']
        year = request.GET['year']
    # else:
    #     month = today.month-1
    #     year = today.year
        # if month!=None and year!=None:
        #     month = today.month
        #     year = today.year
    month = today.month-1
    year = today.year
    print(month)
    monthly_income = Income.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year).aggregate(Sum('amount'))['amount__sum']
    monthly_expense = Expense.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year).aggregate(Sum('amount'))['amount__sum']
    income_category = IncomeCategory.objects.filter(profile=profile)
    monthly_category_wise_income = {}
    monthly_category_wise_income_percent = {}
    for i in income_category:
        income = Income.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year, category=i).aggregate(Sum('amount'))['amount__sum']
        income_list = Income.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year, category=i)
        monthly_category_wise_income[i.name] = income
        if income!=None:
            monthly_category_wise_income_percent[i.name] = round((income/monthly_income)*100, 2)
    monthly_saving = monthly_income - monthly_expense

    expense_category = ExpenseCategory.objects.filter(profile=profile)
    monthly_category_wise_expense = {}   
    monthly_category_wise_expense_percent = {}
    for i in expense_category:
        expense = Expense.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year, category=i).aggregate(Sum('amount'))['amount__sum']
        expense_list = Expense.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year, category=i)
        monthly_category_wise_expense[i.name] = expense
        if expense!=None:
            monthly_category_wise_expense_percent[i.name] = round((expense / monthly_expense)*100, 2)
    template = 'finances/dashboard.html'
    context = {
        'month': month,
        'year': year,
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'monthly_saving': monthly_saving,
        'monthly_category_wise_income': monthly_category_wise_income,
        'monthly_category_wise_expense': monthly_category_wise_expense,
        'monthly_category_wise_expense_percent': monthly_category_wise_expense_percent,
        'monthly_category_wise_income_percent': monthly_category_wise_income_percent,
        'income_list': income_list,
        'expense_list': expense_list,
        'income_category': income_category,
        'expense_category': expense_category
    }
    return render(request, template, context)

####################################################################

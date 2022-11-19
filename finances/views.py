from calendar import month
from nis import cat
from django.shortcuts import render
from django.shortcuts import  redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Income, Expense, IncomeCategory, ExpenseCategory
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Sum
import calendar
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Avg

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
    # get user profile
    profile = User.objects.get(username=username)

    # get month and year (current or user specified)
    today = datetime.date.today()
    month = today.month
    year = today.year
    print(request.GET)
    if 'month' in request.GET and 'year' in request.GET:
        month = request.GET['month']
        year = request.GET['year']

    # get monthly income and expenses
    monthly_income = Income.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year).aggregate(Sum('amount'))['amount__sum']
    monthly_income_details = Income.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year)
    monthly_expense = Expense.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year).aggregate(Sum('amount'))['amount__sum']
    monthly_expense_details = Expense.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year)

    # calculate useful metrics
    if monthly_income!=None:
        if monthly_expense==None:
            monthly_expense = 0
        # monthly savings
        monthly_saving = monthly_income - monthly_expense
        expense_percent = round(monthly_expense*100/monthly_income,2)
        saving_percent = round(monthly_saving*100/monthly_income, 2)

        income_category = IncomeCategory.objects.filter(profile=profile)
        monthly_category_wise_income = {}
        # monthly_category_wise_income_percent = {}

        # monthly category wise income
        for i in income_category:
            income = Income.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year, category=i).aggregate(Sum('amount'))['amount__sum']
            income_list = Income.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year, category=i)
            if income==None:
                income=0
            monthly_category_wise_income[i.name] = income
            # if income!=None:
            #     monthly_category_wise_income_percent[i.name] = round((income/monthly_income)*100, 2)

        # Monthly category wise expense
        expense_category = ExpenseCategory.objects.filter(profile=profile)
        monthly_category_wise_expense = {}   
        monthly_category_wise_expense_percent = {}
        monthly_category_wise_expense_of_income = {'Saving': saving_percent}
        per_day_expense = {}

        for i in expense_category:
            expense = Expense.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year, category=i).aggregate(Sum('amount'))['amount__sum']
            if expense==None:
                expense=0
            expense_list = Expense.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year, category=i)
            monthly_category_wise_expense[i.name] = expense
            if expense!=0:
                monthly_category_wise_expense_percent[i.name] = round((expense / monthly_expense)*100, 2)
                monthly_category_wise_expense_of_income[i.name] = round((expense / monthly_income)*100, 2)
        
            monthly_category_wise_expense = {k: v for k, v in sorted(monthly_category_wise_expense.items(), key=lambda x: x[1], reverse=True)}
            monthly_category_wise_expense_percent = {k: v for k, v in sorted(monthly_category_wise_expense_percent.items(), key=lambda x: x[1], reverse=True)}
            monthly_category_wise_expense_of_income = {k: v for k, v in sorted(monthly_category_wise_expense_of_income.items(), key=lambda x: x[1], reverse=True)}
            monthly_category_wise_income = {k: v for k, v in sorted(monthly_category_wise_income.items(), key=lambda x: x[1], reverse=True)}

            monthly_category_wise_expense_values = list(monthly_category_wise_expense.values())
            monthly_category_wise_expense_keys = list(monthly_category_wise_expense.keys())
            
            monthly_category_wise_expense_percent_values = list(monthly_category_wise_expense_percent.values())
            monthly_category_wise_expense_percent_keys = list(monthly_category_wise_expense_percent.keys())

            monthly_category_wise_expense_of_income_values = list(monthly_category_wise_expense_of_income.values())
            monthly_category_wise_expense_of_income_keys = list(monthly_category_wise_expense_of_income.keys())

            monthly_category_wise_income_values = list(monthly_category_wise_income.values())
            monthly_category_wise_income_keys = list(monthly_category_wise_income.keys())

        # Per day expense
        for day in range(1,32):
            expense = Expense.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year, time_stamp__day=day).aggregate(Sum('amount'))['amount__sum']
            if expense==None:
                expense=0 
            per_day_expense[day]=expense
        per_day_expense_values = list(per_day_expense.values())
        per_day_expense_keys = list(per_day_expense.keys())
        # print(per_day_expense_values)
        # print(per_day_expense_keys)
        daily_average = round(sum(per_day_expense_values)/per_day_expense_keys[-1], 2)
        monthly_average = Expense.objects.filter(profile=profile).annotate(month=ExtractMonth('time_stamp'), year=ExtractYear('time_stamp')).values("month", "year").annotate(total=Sum('amount'))
        monthly_average = [i["total"] for i in monthly_average ]
        monthly_average = round(sum(monthly_average)/len(monthly_average),2)
        # y = Avg(x)
        # print(x, y)
        month = calendar.month_name[int(month)]
        



    # print(monthly_category_wise_income_values)
    # print(monthly_category_wise_income_keys)
    else:
        monthly_saving = None
        monthly_category_wise_income_values = []
        monthly_category_wise_income_keys = []
        monthly_category_wise_expense_values = []
        monthly_category_wise_expense_keys = []
        monthly_category_wise_expense_percent_values = []
        monthly_category_wise_expense_percent_keys = []
        monthly_category_wise_expense_of_income_values = []
        monthly_category_wise_expense_of_income_keys = []
        per_day_expense_values = []
        per_day_expense_keys = []
        income_list = []
        expense_list = []
        income_category = []
        expense_category = []
        expense_percent = []
        saving_percent = []
        monthly_income_details = []
        monthly_expense_details = []
        
        

    template = 'finances/dashboard.html'
    context = {
        'today': today,
        'month': month,
        'year': year,
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'monthly_saving': monthly_saving,

        'monthly_category_wise_income_values': monthly_category_wise_income_values,
        'monthly_category_wise_income_keys': monthly_category_wise_income_keys,

        'monthly_category_wise_expense_values': monthly_category_wise_expense_values,
        'monthly_category_wise_expense_keys': monthly_category_wise_expense_keys,
        # 'monthly_category_wise_expense_percent': monthly_category_wise_expense_percent,
        'monthly_category_wise_expense_percent_values': monthly_category_wise_expense_percent_values,
        'monthly_category_wise_expense_percent_keys': monthly_category_wise_expense_percent_keys,

        # 'monthly_category_wise_income_percent': monthly_category_wise_income_percent,
        'monthly_category_wise_expense_of_income_values': monthly_category_wise_expense_of_income_values,
        'monthly_category_wise_expense_of_income_keys': monthly_category_wise_expense_of_income_keys,

        'income_list': income_list,
        'expense_list': expense_list,
        'income_category': income_category,
        'expense_category': expense_category,
        'expense_percent': expense_percent,
        'saving_percent': saving_percent,
        'monthly_income_details': monthly_income_details,
        'monthly_expense_details': monthly_expense_details,

        'per_day_expense_values': per_day_expense_values,
        'per_day_expense_keys': per_day_expense_keys,
        'daily_average': daily_average,
        'monthly_average': monthly_average

    }
    return render(request, template, context)

####################################################################

# def pie_chart_expense(request):
#     labels = []
#     data = []

#     queryset = City.objects.order_by('-population')[:5]
#     for city in queryset:
#         labels.append(city.name)
#         data.append(city.population)

#     return render(request, 'pie_chart.html', {
#         'labels': labels,
#         'data': data,
#     })

####################################################################

def ExpenseView(request, username=None):
    context ={}
    profile = User.objects.get(username=username)
    category = ExpenseCategory.objects.filter(profile__username=username)
    if 'month' in request.GET and 'year' in request.GET and 'category' in request.GET:
       month = request.GET['month']
       year = request.GET['year'] 
       category = request.GET['category']
       if month=='' and year=='' and category!=None:
           context["expense_list"] = Expense.objects.filter(profile=profile, category=category).order_by('-id')
       elif month!=None and year!=None and category=='':
           context["expense_list"] = Expense.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year).order_by('-id')  
       elif month!=None and year=='' and category:
           return HttpResponse('provide year')
       elif month=='' and year!=None and category:
           return HttpResponse('provide month')
       elif month!=None and year!=None and category!=None:
           context["expense_list"] = Expense.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year, category=category).order_by('-id')  

    # elif 'month' in request.GET and 'year':
    #     month = request.GET['month']
    #     year = request.GET['year'] 
    #     context["expense_list"] = Expense.objects.filter(profile=profile, time_stamp__month=month, time_stamp__year=year)    

    # elif 'category' in request.GET:
    #     category = request.GET['category'] 
    #     context["expense_list"] = Expense.objects.filter(profile=profile, categoty=category)

    else: 
        context["expense_list"] = Expense.objects.filter(profile=profile).order_by('-id')
    context["category_list"] = category
    context["count"] = context["expense_list"].count()
    return render(request, "finances/expense_view.html", context)

####################################################################

def IncomeView(request, username=None):
    context ={}
    profile = User.objects.get(username=username)
    context["income_list"] = Income.objects.filter(profile=profile).order_by('-id')
    return render(request, "finances/income_view.html", context)

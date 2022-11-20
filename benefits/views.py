from django.shortcuts import render
from django.shortcuts import  redirect
from django.contrib.auth.models import User
from .models import Benefits
from django.db.models import Sum


####################################################################

def BenefitsView(request, username=None):
    profile = User.objects.get(username=username)
    if request.method == 'POST':
        time_stamp = request.POST['time_stamp']
        title = request.POST['title']
        amount = request.POST['amount']
        sender = request.POST['sender']
        benefit = Benefits(profile=profile,title=title,amount=amount,sender=sender,time_stamp=time_stamp)
        benefit.save()
        return redirect('benefits:benefit-add-n-list', username=username)
    
    template = 'benefits/benefits.html'
    context ={}
    context["benefit_list"] = Benefits.objects.filter(profile=profile).order_by('-time_stamp')
    context["total_benefit"] = round(Benefits.objects.filter(profile=profile).aggregate(Sum('amount'))['amount__sum'],2)

    return render(request, template, context)

####################################################################

def UpdateBenefitsView(request, username=None, id=None):
    profile = User.objects.get(username=username)
    benefit = Benefits.objects.get(profile__username=username,id=id)
    benefit_update = Benefits.objects.filter(profile__username=username,id=id)

    context = {
        'time_stamp':str(benefit.time_stamp),
        'title':benefit.title,
        'amount':benefit.amount,
        'sender':benefit.sender,
    }

    # print(str(income.time_stamp))
    if request.method == 'POST':
        time_stamp = request.POST['time_stamp']
        title = request.POST['title']
        amount = request.POST['amount']
        sender = request.POST['sender']
        benefit_update.update(profile=profile,title=title,amount=amount,sender=sender,time_stamp=time_stamp)
        return redirect('benefits:benefit-add-n-list', username=username)
    template = 'benefits/update_benefit.html'
    return render(request, template, context)

####################################################################
def DeleteBenefitsView(request, username=None, id=None):
    Benefits.objects.filter(profile__username=username,id=id).delete()
    return redirect('benefits:benefit-add-n-list', username=username)

####################################################################
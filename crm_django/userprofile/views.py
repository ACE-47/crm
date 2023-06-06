from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse

from team.models import Team
from .models import Userprofile
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Userprofile.objects.create(user = user )
            # login_url = reverse('userprofile:login')
            team =Team.objects.create(name = 'the name team',created_by = request.user)
            team.member.aadd(request.user)
            team.save()
            return redirect('/userprofile/log-in/')
    else:
        form =UserCreationForm()

    return render(request,'userprofile/signup.html',{
        'form':form,
    })


@login_required
def account(request):
    team = Team.objects.filter(created_by = request.user)[0]
    return render(request,'userprofile/myaccount.html',{
        'team':team,
    })
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from team.models import Team
from .models import Userprofile
from .forms import SignUpForm
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login_url = reverse('userprofile:login')
            team =Team.objects.create(name = 'the name team',created_by = user)
            team.member.aadd(user)
            team.save()
            Userprofile.objects.create(user = user, active_team = team )
            return redirect('/userprofile/log-in/')
    else:
        form =SignUpForm()

    return render(request,'userprofile/signup.html',{
        'form':form,
    })


@login_required
def account(request):
    team = Team.objects.filter(created_by = request.user)[0]
    return render(request,'userprofile/myaccount.html',{
        'team':team,
    })
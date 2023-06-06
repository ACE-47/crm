from typing import Any
from django import http
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from team.models import Team
from .forms import AddLeadForm
from .models import Lead
from client.models import Client  # imported like mosh said
# Create your views here.

class LeadListView(ListView):
    model =Lead
    context_object_name = 'leads'
    template_name = 'lead/leads_list.html'

    @method_decorator(login_required)
    def dispatch(self,  *args, **kwargs) :
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset =  super(LeadListView, self).get_queryset()
        queryset = queryset.filter(created_by =self.request.user,converted_to_client = False)
        return queryset
    
##############################

class LeadDetailView(DetailView):
    model = Lead
    template_name = 'lead/lead_details.html'

    @method_decorator(login_required)
    def dispatch(self,  *args, **kwargs) :
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset =  super(LeadDetailView).get_queryset()
        queryset = queryset.filter(created_by =self.request.user,pk = self.kwargs.get('pk'))
        return queryset
    
##############################################


# @login_required
# def leads_list(request):
#     leads = Lead.objects.filter(created_by = request.user,converted_to_client = False)
#     return render(request,'lead/leads_list.html',{
#         'leads':leads,
#     })


@login_required
def lead_delete(request,pk):
    lead = get_object_or_404(Lead,created_by = request.user,pk = pk)
    lead.delete()

    messages.success(request, 'The lead was successfuly deleted')
    return redirect('leads-list')

@login_required
def edit_lead(request,pk):
    lead = get_object_or_404(Lead,created_by = request.user,pk = pk)

    if request.method == 'POST':
        form = AddLeadForm(request.POST,instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, 'The changes were successfuly updated')
            return redirect('leads-list')
    else:
        form = AddLeadForm(instance=lead)
    
    return render(request,'lead/edit_lead.html',{
        'form':form
    })



# @login_required
# def lead_details(request, pk):
#     lead = get_object_or_404(Lead,created_by = request.user,pk = pk)
   
#     return render(request,'lead/lead_details.html',{
#         'lead':lead
#     })

@login_required
def add_lead(request):
    # make the logic of checking the max leads in here rother than in the template or both .............................
    team = Team.objects.filter(created_by = request.user)[0]
    if request.method == 'POST':
        form =AddLeadForm(request.POST)
        if form.is_valid():
            team = Team.objects.filter(created_by = request.user)[0]
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.team =team
            lead.save()
            messages.success(request, 'The lead was successfuly created')
            return redirect('leads-list')
    else:
        form = AddLeadForm()
    return render(request,'lead/add_lead.html',{
        'form':form,
        'team':team
    })


@login_required
def convert_to_client(request,pk):
    lead = get_object_or_404(Lead,created_by = request.user,pk = pk)
    team = Team.objects.filter(created_by = request.user)[0]

    client = Client.objects.create(name = lead.name,
                                   email = lead.email,
                                   description = lead.description,
                                   created_by = request.user,
                                   team = team
                                   )
    
    lead.converted_to_client = True
    lead.save()
    messages.success(request, 'The lead was successfuly converted into a client')
    return redirect('leads-list')
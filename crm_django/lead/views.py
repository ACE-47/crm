from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404 
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView,View
from team.models import Team
from .forms import AddCommentForm, AddFileForm
from .models import Lead
from client.models import Client, Comment as ClientComment  # imported like mosh said
# Create your views here.

class LeadListView(LoginRequiredMixin,ListView):
    model =Lead
    context_object_name = 'leads'
    template_name = 'lead/leads_list.html'

    # @method_decorator(login_required)
    # def dispatch(self,  *args, **kwargs) :
    #     return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset =  super(LeadListView, self).get_queryset()
        queryset = queryset.filter(created_by =self.request.user,converted_to_client = False)
        return queryset
    
##############################

class LeadDetailView(LoginRequiredMixin,DetailView):
    model = Lead
    template_name = 'lead/lead_details.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['formfile'] = AddFileForm()
        return context
    

    # @method_decorator(login_required)
    # def dispatch(self,  *args, **kwargs) :
    #     return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset =  super(LeadDetailView,self).get_queryset()
        queryset = queryset.filter(created_by =self.request.user,pk = self.kwargs.get('pk'))
        return queryset
    
##############################################

class LeadDeleteView(LoginRequiredMixin,DeleteView):
    model = Lead
    success_url = reverse_lazy('leads-list')

    # @method_decorator(login_required)
    # def dispatch(self,  *args, **kwargs) :
    #     return super().dispatch(*args, **kwargs)
    

    def get_queryset(self):
        queryset =  super(LeadDeleteView,self).get_queryset()
        queryset = queryset.filter(created_by =self.request.user, pk = self.kwargs.get('pk'))
        return queryset

    # def get(self, request, *args, **kwargs) -> HttpResponse:
    #     return self.post(request, *args, **kwargs)

##########################################################

class LeadUpdateView(LoginRequiredMixin,UpdateView):
    model = Lead
    fields = ('name','email','description','priority','status')

    template_name = 'lead/lead_form.html'
    success_url = reverse_lazy('leads-list')

    # @method_decorator(login_required)
    # def dispatch(self,  *args, **kwargs) :
    #     return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset =  super(LeadUpdateView,self).get_queryset()
        queryset = queryset.filter(created_by =self.request.user, pk = self.kwargs.get('pk'))
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Lead'
        return context
    
##############################################

class LeadCreateView(LoginRequiredMixin,CreateView):
    model = Lead
    fields = ('name','email','description','priority','status')

    template_name = 'lead/lead_form.html'
    success_url = reverse_lazy('leads-list')

    # @method_decorator(login_required)
    # def dispatch(self,  *args, **kwargs) :
    #     return super().dispatch(*args, **kwargs)
    
    
    
    def form_valid(self, form: BaseModelForm) :
        team = Team.objects.filter(created_by = self.request.user)[0]
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = team
        self.object.save()
        return redirect(self.get_success_url())
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by = self.request.user)[0]
        context['team'] = team
        context['title'] = 'Add Lead'
        return context
    

class ConvertToClientView(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        lead = get_object_or_404(Lead,created_by = request.user,pk = kwargs.get('pk'))
        team = Team.objects.filter(created_by = request.user)[0]

        client = Client.objects.create(name = lead.name,
                                    email = lead.email,
                                    description = lead.description,
                                    created_by = request.user,
                                    team = team
                                    )
        
        lead.converted_to_client = True
        lead.save()
        
        #convert lead comments to the client  
        for comment in lead.comments.all():
            ClientComment.objects.create(
                content = comment.content,
                created_by = comment.created_by,
                team = team,
                client = client,
            )


        messages.success(request, 'The lead was successfuly converted into a client')
        return redirect('leads-list')
    

class AddFileView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        form = AddFileForm(request.POST,request.FILES)
        if form.is_valid():
            team = Team.objects.filter(created_by = request.user)[0]
            file = form.save(commit=False)
            file.team = team 
            file.lead_id = pk
            file.created_by = request.user
            file.save()
        
        return redirect('lead-details',pk=pk)
        


class AddCommentView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        
        form = AddCommentForm(request.POST)
        pk = kwargs.get('pk')
        

        if form.is_valid():
            team = Team.objects.filter(created_by = request.user)[0]
            comment = form.save(commit=False)
            comment.created_by = request.user
            comment.team = team
            comment.lead_id = pk
            
            comment.save()

        return redirect('lead-details',pk = pk)
# @login_required
# def leads_list(request):
#     leads = Lead.objects.filter(created_by = request.user,converted_to_client = False)
#     return render(request,'lead/leads_list.html',{
#         'leads':leads,
#     })


# @login_required
# def lead_delete(request,pk):
#     lead = get_object_or_404(Lead,created_by = request.user,pk = pk)
#     lead.delete()

#     messages.success(request, 'The lead was successfuly deleted')
#     return redirect('leads-list')


# @login_required
# def edit_lead(request,pk):
#     lead = get_object_or_404(Lead,created_by = request.user,pk = pk)

#     if request.method == 'POST':
#         form = AddLeadForm(request.POST,instance=lead)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'The changes were successfuly updated')
#             return redirect('leads-list')
#     else:
#         form = AddLeadForm(instance=lead)
    
#     return render(request,'lead/edit_lead.html',{
#         'form':form
#     })



# @login_required
# def lead_details(request, pk):
#     lead = get_object_or_404(Lead,created_by = request.user,pk = pk)
   
#     return render(request,'lead/lead_details.html',{
#         'lead':lead
#     })

# @login_required
# def add_lead(request):
#     # make the logic of checking the max leads in here rother than in the template or both .............................
#     team = Team.objects.filter(created_by = request.user)[0]
#     if request.method == 'POST':
#         form =AddLeadForm(request.POST)
#         if form.is_valid():
#             team = Team.objects.filter(created_by = request.user)[0]
#             lead = form.save(commit=False)
#             lead.created_by = request.user
#             lead.team =team
#             lead.save()
#             messages.success(request, 'The lead was successfuly created')
#             return redirect('leads-list')
#     else:
#         form = AddLeadForm()
#     return render(request,'lead/add_lead.html',{
#         'form':form,
#         'team':team
#     })


# @login_required
# def convert_to_client(request,pk):
#     lead = get_object_or_404(Lead,created_by = request.user,pk = pk)
#     team = Team.objects.filter(created_by = request.user)[0]

#     client = Client.objects.create(name = lead.name,
#                                    email = lead.email,
#                                    description = lead.description,
#                                    created_by = request.user,
#                                    team = team
#                                    )
    
#     lead.converted_to_client = True
#     lead.save()
#     messages.success(request, 'The lead was successfuly converted into a client')
#     return redirect('leads-list')


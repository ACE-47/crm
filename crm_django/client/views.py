from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team.models import Team
from .models import Client
from .forms import AddClientForm, AddCommentForm, AddFileForm
# Create your views here.

def clients_list(request):
    clients = Client.objects.filter(created_by = request.user)
    return render(request,'client/clients_list.html',{
        'clients':clients
    })


@login_required
def client_details(request, pk):
    client = get_object_or_404(Client, created_by = request.user, pk = pk)
    team = Team.objects.filter(created_by = request.user)[0]
    formfile = AddFileForm()

    if request.method == 'POST':

        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_by = request.user
            comment.team = team
            comment.client = client
            comment.save()
            return redirect('client-details',pk = pk)
    else:
        form = AddCommentForm()
    return render(request,'client/client_detail.html',{
        'client':client,
        'form': form,
        'formfile':formfile
    })

@login_required
def add_file(request, pk):
    team = Team.objects.filter(created_by = request.user)[0]
    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.team = team
            file.created_by = request.user
            file.client_id = pk
            file.save()
        return redirect('client-details',pk=pk)


@login_required
def add_client(request):
    team = Team.objects.filter(created_by = request.user)[0]
    if request.method == 'POST':
        form =AddClientForm(request.POST)
        if form.is_valid():
            # change how the team was chosen
            team = Team.objects.filter(created_by = request.user)[0]
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()
            messages.success(request, 'The Client was successfuly created')
            return redirect('clients-list')
    else:
        form = AddClientForm()
    return render(request,'client/add_client.html',{
        'form':form,
        'team':team
    })


@login_required
def delete_client(request, pk):
    client = get_object_or_404(Client, created_by = request.user, pk = pk)
    client.delete()

    messages.success(request, 'The Client was successfuly deleted')
    return redirect('clients-list')


@login_required
def edit_client(request,pk):
    client = get_object_or_404(Client, created_by = request.user, pk = pk)

    if request.method == 'POST':
        form = AddClientForm(request.POST,instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'The changes were successfuly updated')
            return redirect('clients-list')
    else:
        form = AddClientForm(instance=client)
    
    return render(request,'client/edit_client.html',{
        'form':form
    })
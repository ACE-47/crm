from .models import Team

def active_team(request):
    team =Team.objects.filter(created_by = request.user)[0]

    return {'active_team':team}
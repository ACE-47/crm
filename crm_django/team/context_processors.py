from .models import Team

def active_team(request):
    if request.user.is_authenticated:
        team =Team.objects.filter(created_by = request.user)[0]
    else:
        team = None
    return {'active_team':team}
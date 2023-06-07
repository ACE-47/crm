from django.contrib.auth.models import User
from django.db import models

from team.models import Team #do as mosh said

# Create your models here.

class Client(models.Model):
    team = models.ForeignKey(Team, related_name='clients', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE , related_name='clients')
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    

class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='clients_comment',on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE , related_name='clients_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by
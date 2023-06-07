from django.contrib.auth.models import User
from django.db import models

from team.models import Team #  do as mosh said

# Create your models here.

class Lead(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    CHOICES_PRIORITY = (
        (LOW , 'Low'),
        (MEDIUM , 'Medium'),
        (HIGH , 'High'),
        )
    

    NEW = 'new'
    CONTACTED = 'contacted'
    LOST = 'lost'
    WON ='won'

    CHOICES_STATUS = (
        (NEW , 'New'),
        (CONTACTED , 'Contacted'),
        (LOST , 'Lost'),
        (WON , 'Won'),
        )
    
    team = models.ForeignKey(Team, related_name='leads',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE , related_name='leads')
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10,choices=CHOICES_PRIORITY,default=MEDIUM)
    status = models.CharField(max_length=10,choices=CHOICES_STATUS,default=NEW)
    modified = models.DateTimeField(auto_now=True)
    converted_to_client = models.BooleanField(default=False) 

    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    

class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='leads_comment',on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE , related_name='lead_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by
    
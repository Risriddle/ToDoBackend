from django.db import models
from django.contrib.auth.models import User

# Create your models here.
'''class UserData(models.Model):
    name=models.CharField(max_length=50)
    pwd=models.CharField(max_length=8)
    #human readable in admin panel
    def __str__(self):
        return self.name'''
    
class TodoUsers(models.Model):
    username =  models.ForeignKey(User,on_delete=models.CASCADE)
    #password= models.IntegerField(default=10,null=True)
    due_date=models.DateTimeField(auto_now_add=True,null=True)
    #date_created=models.DateTimeField(auto_now_add=True,null=True)
    todo=models.CharField(max_length=50,null=True)
    
    def __str__(self):
        return self.username.username
        
    
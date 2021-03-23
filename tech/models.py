from django.db import models
from membership.models import *
# Create your models here.


class TaskAssignToUser(models.Model):
    assignedTo =\
    models.ForeignKey(TechPerson,related_name='task_assign',on_delete=models.CASCADE)
    workedBy =\
    models.ManyToManyField(TechPerson,related_name='users_assign',blank=True,null=True)
    task_title = models.CharField(max_length=500,blank=True,null=True)
    task = models.TextField()
    taskStart_date = models.DateTimeField(blank=True,null=True)
    taskEnd_date = models.DateTimeField(blank=True,null=True)
    teck_user_issues = models.TextField(blank=True,null=True)
    is_task_ongoing = models.BooleanField(default=False)
    
    def __str__(self):
        return self.task_title


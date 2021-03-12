from django.db import models
from django.utils import timezone
from membership.models import *
# Create your models here.


class Lead(models.Model):
    personName = models.CharField(max_length=100)
    instituteName = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateTimeField(default=timezone.now())
    contactPhone = models.TextField(blank=True,null=True)
    email = models.EmailField(max_length=500,blank=True,null=True)
    numberStudents = models.CharField(max_length=20,blank=True,null=True)
    location = models.CharField(max_length=2000,blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    source = models.CharField(max_length=1000,blank=True,null=True)
    assignedTo =\
    models.ForeignKey(SalesExecutive,related_name='lead_assign',blank=True,null=True,on_delete=models.CASCADE)
    workedBy =\
    models.ManyToManyField(SalesExecutive,related_name='lead_second_assign')


    def __str__(self):
        return self.personName


class FeedBack(models.Model):
    typeFeedBack = models.IntegerField()
    by = \
    models.ForeignKey(SalesExecutive,related_name='feedback_person',blank=True,null=True,on_delete=models.CASCADE)
    lead =\
    models.ForeignKey(Lead,related_name='feeback_lead',on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now())
    rating = models.IntegerField()
    notes = models.TextField()
    nextCall = \
    models.ForeignKey(SalesExecutive,related_name='feedback_nextcall',blank=True,null=True,on_delete=models.CASCADE)
    nextCallDate = models.DateTimeField(blank=True,null=True)
    demo = models.BooleanField(default = False)
    demoDate = models.DateTimeField(blank=True,null=True)
    feedback = models.CharField(max_length=100)
    furtherCall = models.BooleanField()
    priceQuoted = models.FloatField(default=12000)

    def __str__(self):
        return self.by.name

    # def __str__(self):
    #     return self.by.name + ' ' + str(lead.personName)


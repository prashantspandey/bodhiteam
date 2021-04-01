from django.db import models
from django.utils import timezone
from membership.models import *
from django.core.validators import MaxValueValidator
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
    models.ManyToManyField(SalesExecutive,related_name='lead_second_assign',blank=True,null=True)

    def __str__(self):
        return self.personName

class SuccessfullyLead(models.Model):
    by = models.ForeignKey(SalesExecutive,on_delete=models.SET_NULL,blank=True,null=True)
    lead = models.ForeignKey(Lead,related_name='comfirmed_lead',on_delete=models.SET_NULL,blank=True,null=True)
    priceQuoted = models.CharField(max_length=200)
    extra_requirement = models.TextField(blank=True,null=True)
    datetime = models.DateTimeField(default=timezone.now())


class FeedBack(models.Model):
    typeFeedBack = models.IntegerField()
    by = \
    models.ForeignKey(SalesExecutive,related_name='feedback_person',blank=True,null=True,on_delete=models.CASCADE)
    lead =\
    models.ForeignKey(Lead,related_name='feeback_lead',on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now())
    rating = models.IntegerField()
    notes = models.TextField()
    Cource = models.CharField(max_length=200,blank=True,null=True)
    instituteType = models.CharField(max_length=200,blank=True,null=True)
    State = models.CharField(max_length=200,blank=True,null=True)
    city = models.CharField(max_length=200,blank=True,null=True)
    Is_wrongLead = models.BooleanField(default=False)
    nextCall = \
    models.ForeignKey(SalesExecutive,related_name='feedback_nextcall',blank=True,null=True,on_delete=models.CASCADE)
    nextCallDate = models.DateTimeField(blank=True,null=True)
    demo = models.BooleanField(default = False)
    demoDate = models.DateTimeField(blank=True,null=True)
    feedback = models.CharField(max_length=100)
    furtherCall = models.BooleanField()
    priceQuoted = models.CharField(max_length=200,blank=True,null=True,default=12000)

    def __str__(self):
        return self.by.name + ' ' + self.lead.personName
        
class DemoFeedback(models.Model):
    typedemo = models.IntegerField()
    by = models.ForeignKey(SalesExecutive, related_name='demo_person', blank=True, null=True,on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, related_name='demo_lead', on_delete=models.CASCADE)
    demo_rating = models.IntegerField(validators=[MaxValueValidator(5)])
    demo_feedback = models.CharField(max_length=100)
    extra_notes = models.TextField(blank=True,null=True)
    price_quoted = models.FloatField(default=12000)
    datetime = models.DateTimeField(default=timezone.now())
    demo_nextCall = models.ForeignKey(SalesExecutive, related_name='demo_nextcall', blank=True, null=True,on_delete=models.CASCADE)
    demo_nextCallDate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.by.name + ' ' + self.lead.personName

    class Meta:
        verbose_name = "DemoFeedback"
        verbose_name_plural = "DemoFeedbacks"

class Massages(models.Model):
    senderId = models.ForeignKey(SalesExecutive, related_name='sender',on_delete=models.CASCADE)
    reciverId = models.ForeignKey(SalesExecutive, related_name='reciever', on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead,on_delete=models.SET_NULL,blank=True,null=True)
    feedback = models.ForeignKey(FeedBack,on_delete=models.SET_NULL,blank=True,null=True)
    massage = models.TextField(blank=True,null=True)
    massagRead = models.BooleanField(default=False) 
    datetime = models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return self.senderId.name 

    class Meta:
        verbose_name = "Massage"
        verbose_name_plural = "Massages"

class Notification(models.Model):
    notification_user = models.ForeignKey(SalesExecutive, related_name='user_notification',on_delete=models.CASCADE)
    sender_user = models.ForeignKey(SalesExecutive, related_name='MessageSender_name', on_delete=models.CASCADE)
    massage = models.TextField(blank=True,null=True)
    is_FirstTime = models.BooleanField(default=True) 
    datetime = models.DateTimeField(default=timezone.now())

class DemoFeedback_And_LeadFeedback_Notifications(models.Model):
    notification_user = models.ForeignKey(SalesExecutive, related_name='demofeedbackuser_notification',on_delete=models.CASCADE)
    sender_user = models.ForeignKey(SalesExecutive, related_name='DemoAssigner_name', on_delete=models.SET_NULL,blank=True,null=True)
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=100)
    massage = models.TextField(blank=True,null=True)
    is_FirstTime = models.BooleanField(default=True)
    nextDate = models.DateTimeField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.localtime())

    def __str__(self):
        return self.notification_user.name
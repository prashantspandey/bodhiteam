from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class SalesExecutive(models.Model):
    executiveUser = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    photo = models.URLField(blank=True,null=True)
    joiningDate = models.DateField()
    typeExecutive = models.CharField(max_length=50)
    salesNumber = models.IntegerField(blank=True,null=True)
    contact = models.CharField(blank=True,null=True,max_length=12)
    email = models.EmailField(blank=True,null=True)
    address = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return self.name + ' ' + self.typeExecutive

class Technology(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TechPerson(models.Model):
    executiveUser = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    photo = models.URLField()
    joiningDate = models.DateField()
    typeTech = models.CharField(max_length=50)
    technology = models.ManyToManyField(Technology)

    def __str__(self):
        return self.name + ' ' + self.typeTech





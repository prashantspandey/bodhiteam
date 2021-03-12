from django.contrib import admin
from django.urls import path
from .models import *
from . import views
app_name = 'sales'
urlpatterns = [
    path('upload_csv',views.lead_upload,name='uploadLoad'),

]

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .models import *
from . import views
app_name = 'sales'

urlpatterns = [
    path('upload_csv',views.lead_upload,name='uploadLoad'),
    path('login',views.loginView,name='login'),
    path('logout',views.logoutview,name='logout'),
    path('Get_my_all_leads',views.GetMyAllLeadView,name='Get_my_all_leads'),
    path('Get_my_worked_leads',views.GetMyWorkedLeadsView,name='Get_my_worked_leads'),
    url(r'feedback/$',views.FeedbackCreateView.as_view(),name='feedback'),
]

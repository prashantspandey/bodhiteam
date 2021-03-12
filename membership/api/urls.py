from django.conf.urls import url
from django.urls import path
from membership.models import *
from membership.api import views



urlpatterns = [
    url(r'login/$',views.Login.as_view(),name='login'),

]

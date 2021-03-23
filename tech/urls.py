from django.urls import path
from django.conf.urls import url
from . import views
app_name = 'tech'

urlpatterns = [
    path('Get_Mynewtask/',views.GetMyNewTaskView,name='Get_Mynewtask'),
    path('edit_task/',views.EditTaskView,name='edit_task'),
]

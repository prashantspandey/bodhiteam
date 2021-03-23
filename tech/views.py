from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.contrib import messages
from .models import * 
# Create your views here.

def GetMyNewTaskView(request):
    newTasks = TaskAssignToUser.objects.filter(assignedTo=request.user.techperson)
    return render(request,'tech/NewTask.html',{'newTasks':newTasks})

def EditTaskView(request):
    if request.method == "POST": 
        updatetask = TaskAssignToUser.objects.get(id=request.POST.get('task_id'))
        updatetask.teck_user_issues = request.POST.get('user_issue')
        updatetask.taskEnd_date = request.POST.get('task_enddate')
        if request.POST.get('is_task_ongoing')  == 'on':
            updatetask.is_task_ongoing = True
        else:
            updatetask.is_task_ongoing = False
        updatetask.save()
        messages.success(request, 'Successfully')
        return redirect('/tech/Get_Mynewtask/') 
    else:    
        get_task_for_edit = TaskAssignToUser.objects.get(id=request.GET['task_id'])
        return render(request,'tech/EditTask.html',{'get_task_for_edit':get_task_for_edit})

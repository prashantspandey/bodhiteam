from django.shortcuts import render,redirect
from membership.models import SalesExecutive,TechPerson
from django.contrib import messages
from sales.models import *
# Create your views here.

def IndexView(request):
    if request.user.is_authenticated:
        try:
            request.user.salesexecutive 
            user_notification = Notification.objects.filter(notification_user=request.user.salesexecutive,is_FirstTime=True)
            return render(request,'Index.html',{'user_notification':user_notification})
        except:
            try:
                request.user.techperson
                return render(request,'Index.html')
            except:
                messages.success(request, 'Inside Only sales or teck user allowed ..and you are not a sales or teck user')
                return redirect('/sales/login')
    else:
        return redirect('/sales/login')
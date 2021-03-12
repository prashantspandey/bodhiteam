from django.shortcuts import render,redirect
from membership.models import SalesExecutive
from django.contrib import messages
# Create your views here.

def IndexView(request):
    if request.user.is_authenticated:
        try:
            request.user.salesexecutive
            return render(request,'Index.html')
        except:
            messages.success(request, 'Inside Only sales or teck user allowed ..and you are not a sales or teck user')
            return redirect('/sales/login')
    else:
        return redirect('/sales/login')
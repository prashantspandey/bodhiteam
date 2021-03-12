from django.shortcuts import render,redirect

# Create your views here.

def IndexView(request):
    if request.user.is_authenticated:
        return render(request,'Index.html')
    else:
        return redirect('/sales/login')
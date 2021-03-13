from django.shortcuts import render,redirect
import csv, io
import pandas as pd
from .models import *
from membership.models import *
from django.http import HttpResponse
from django.contrib.auth.models import auth ,User
from django.views.generic.base import View
from django.contrib import messages
import datetime
# Create your views here.


def lead_upload(request):
    template = 'sales/lead_upload.html'
    if request.method == 'GET':
        return render(request,template,{})
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'This is not csv')
    df = pd.read_csv(csv_file)
    final_list = []
    sources = df['Source']
    notes = df['Notes']
    name = df['Client Name']
    phone = df['Phone Number']
    email = df['Email']
    final_list = list(zip(sources,name,phone,email,notes))
    for so,na,ph,em,no in final_list:
        lead = Lead.objects.filter(contactPhone=ph)
        if len(lead) > 0:
            continue
        else:
            number_students = 0
            type_educatior = ''
            details = no.split('\n')
            for det in details:
                if 'Educator' in det:
                    type_educator = det.split(':')[1]
                if 'Students' in det:
                    number_students = det.split(':')[1]
            leads =\
            Lead(personName=na,source=so,contactPhone=ph,email=em,numberStudents=number_students,notes=type_educator)
            leads.save()
    #data_set = csv_file.read().decode('UTF-8')
    #io_string = io.StringIO(data_set)
    #next(io_string)
    #for column in csv.reader(io_string,delimiter=',',quotechar="|"):
    #    print('type column {}'.format(type(column)))
    #    for col in column:
    #        print(col)
    #    #print('source {}'.format(column[0]))
    #    #print('whatsapp number {}'.format(column[1]))
    #    #print('display name {}'.format(column[2]))
    #    #print('date {}'.format(column[3]))
    #    #print('name {}'.format(column[4]))
    #    #print('notes {}'.format(column[6]))
    context = {}
    return render(request,template,context)

def loginView(request):
    if request.method == 'GET':
        return render(request,'sales/login.html')
    else:
        username = request.POST.get("UserName")
        password = request.POST.get("Password")        
        try:
            user = auth.authenticate(request,username=username,password=password)
            auth.login(request, user)
            return redirect('/')
        except:
            messages.error(request, 'Invalid user')
            return redirect('/sales/login',)

def GetMyNewLeadView(request):
    try:
        request.user.salesexecutive
        leads = Lead.objects.filter(assignedTo=request.user.salesexecutive).order_by('-date')
        leads_list = []
        for i in leads:
            if not FeedBack.objects.filter(lead=i.id).exists():
                leads_list.append(leads.get(id=i.id))
        return render(request,'sales/lead.html',{"leads":leads_list})
    except:
        return redirect('/sales/login')

def GetMyWorkedLeadsView(request):
    try:
        request.user.salesexecutive
        leads = Lead.objects.filter(assignedTo=request.user.salesexecutive).order_by('-date')
        leads_list = []
        for i in leads:
            if FeedBack.objects.filter(lead=i.id).exists():
                lead = leads.get(id=i.id)
                leads_list.append(lead)
        return render(request, 'sales/Workedleads.html', {'allworkedleads': leads_list})
    except:
        return redirect('/sales/login')

class FeedbackCreateView(View):
    def get(self,request):
        users = SalesExecutive.objects.all()
        return render(request,'sales/Feedback.html',{'SalesExecutiveUser':users})

    def post(self,request):
        demo = request.POST.get("demo")
        furthercall = request.POST.get("furthercall")
        lead_id = request.POST.get('next')

        my_profile = self.request.user.salesexecutive
        lead = Lead.objects.get(id=lead_id)

        feedback = FeedBack(typeFeedBack=request.POST.get("TypeFeedBack"),by=my_profile,lead=lead,time= datetime.datetime.now(),
                            rating=request.POST.get("rating"),notes=request.POST.get("notes"),)

        if request.POST.get("nextcalluser"):
            executive = SalesExecutive.objects.get(id=request.POST.get("nextcalluser"))
            feedback.nextCall = executive
        else:
            feedback.nextCall = None
        if request.POST.get("nextcalldate"):
            feedback.nextCallDate = request.POST.get("nextcalldate")
        else:
            feedback.nextCallDate = None

        if request.POST.get("demodate"):
            feedback.demoDate = request.POST.get("demodate")
        else:
            feedback.demoDate = None
        if demo == 'on':
            feedback.demo = True
        else:
            feedback.demo = False

        feedback.feedback = request.POST.get("feedback")
        if furthercall == 'on':
            feedback.furtherCall = True
        else:
            feedback.furtherCall = False
        feedback.priceQuoted = request.POST.get("pricequoted")
        feedback.save()
        messages.success(request, 'Feedback saved successfully')
        return redirect('/')

class DemoCreatingView(View):
    def get(self,request):
        users = SalesExecutive.objects.all()
        return  render(request,'sales/DemoCreating.html',{'SalesExecutiveUser':users})
    def post(self,request):
        lead_id = request.POST.get('next')
        my_profile = self.request.user.salesexecutive
        lead = Lead.objects.get(id=lead_id)
        demofeedback = DemoFeedback(typedemo=request.POST.get("typedemo"), by=my_profile, lead=lead,
                            datetime=datetime.datetime.now(),
                            demo_rating=request.POST.get("demo_rating"), extra_notes=request.POST.get("extra_notes"),
                                    demo_feedback=request.POST.get("demo_feedback"),price_quoted = request.POST.get("price_quoted"))
        if request.POST.get("demo_nextCall"):
            demofeedback.demo_nextCall = SalesExecutive.objects.get(id=request.POST.get("demo_nextCall"))
        else:
            demofeedback.demo_nextCall = None

        if request.POST.get("demo_nextCallDate"):
            demofeedback.demo_nextCallDate = request.POST.get("demo_nextCallDate")
        else:
            demofeedback.demo_nextCallDate = None
        demofeedback.save()
        messages.success(request, 'demofeedback saved successfully')
        return redirect('/')

def GetMyFeedbackesLeadWise(request,lead_id):
    feedbacks = FeedBack.objects.filter(lead=lead_id)
    demos = DemoFeedback.objects.filter(lead=lead_id)
    return render(request,'sales/ALlFeedbackes.html',{'feedbackes':feedbacks,'demos':demos})

def logoutview(request):
    auth.logout(request)
    messages.success(request, 'Logged Out Successfully')
    return redirect('/sales/login')
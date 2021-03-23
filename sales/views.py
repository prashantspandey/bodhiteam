from django.shortcuts import render,redirect
import csv, io
import pandas as pd
from .models import *
from membership.models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import auth ,User
from django.views.generic.base import View
from django.contrib import messages
import datetime
from django.db.models import Prefetch
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
        user = None
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            try:
                User.objects.get(username=username)
                messages.error(request, 'Incorrect Password')
                return redirect('/sales/login')
            except User.DoesNotExist:
                messages.error(request, 'Incorrect Username')
                return redirect('/sales/login')

def GetMyNewLeadView(request):
    try:
        request.user.salesexecutive
        leads = Lead.objects.filter(assignedTo=request.user.salesexecutive).prefetch_related('feeback_lead').order_by('-date')
        leads_list = []
        for i in leads:
            if not i.feeback_lead.filter(lead=i.id).exists():
                leads_list.append(i)
        return render(request,'sales/lead.html',{"leads":leads_list})
    except:
        return redirect('/sales/login')

def GetMyWorkedLeadsView(request):
    try:
        request.user.salesexecutive
        leads = Lead.objects.filter(assignedTo=request.user.salesexecutive).prefetch_related('feeback_lead').order_by('-date')
        leads_list = []
        for i in leads:
            if i.feeback_lead.filter(lead=i.id).exists():
                leads_list.append(i)
        return render(request, 'sales/Workedleads.html', {'allworkedleads': leads_list})
    except:
        return redirect('/sales/login')

class FeedbackCreateView(View):
    def get(self,request):
        users = SalesExecutive.objects.all()
        return render(request,'sales/Feedback.html',{'SalesExecutiveUser':users})

    def post(self,request):
        demo = request.POST.get("demo")
        iswronglead = request.POST.get("iswronglead")
        furthercall = request.POST.get("furthercall")
        lead_id = request.POST.get('lead_id')

        my_profile = self.request.user.salesexecutive
        lead = Lead.objects.get(id=lead_id)

        feedback = FeedBack(typeFeedBack=FeedBack.objects.filter(lead=lead_id).count()+1,by=my_profile,lead=lead,time= datetime.datetime.now(),
                            rating=request.POST.get("rating"),notes=request.POST.get("notes"),Cource=request.POST.get("Course"),
                            instituteType=request.POST.get("instituteType"),State=request.POST.get("state"),city=request.POST.get("city"))

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

        if iswronglead == 'on':
            feedback.Is_wrongLead = True
        else:
            feedback.Is_wrongLead = False
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
        lead_id = request.POST.get('lead_id')
        my_profile = self.request.user.salesexecutive
        lead = Lead.objects.get(id=lead_id)

        demofeedback = DemoFeedback(typedemo=DemoFeedback.objects.filter(lead=lead_id).count()+1, by=my_profile, lead=lead,
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

class SendMassageToUserView(View):
    def get(self,request):
        leads = None
        users = SalesExecutive.objects.prefetch_related('lead_assign').all()
        for i in users:
            if i.lead_assign.filter(assignedTo=self.request.user.salesexecutive).exists():
                leads = i.lead_assign.filter(assignedTo=self.request.user.salesexecutive).order_by('-date')
                break
        context = {'SalesExecutiveUser':users,'leads':leads}
        return render(request,'sales/MassageForm.html',context)
    
    def post(self,request):
        lead_id = request.POST.get('sendinglead')
        Lead_Feedback_Id = request.POST.get('feedback')
        if Lead_Feedback_Id:
            Lead_Feedback_Id = FeedBack.objects.get(id=Lead_Feedback_Id) 
        else:
            Lead_Feedback_Id = None
        if lead_id:
            lead_id = Lead.objects.get(id=lead_id)
        else:
            lead_id = None
        Massages.objects.create(senderId=self.request.user.salesexecutive,reciverId=SalesExecutive.objects.get(id=request.POST.get('reciver')),lead=lead_id,feedback=Lead_Feedback_Id,massage=request.POST.get('massage'),datetime=datetime.datetime.now())
        
        get,create = Notification.objects.get_or_create(notification_user=SalesExecutive.objects.get(id=request.POST.get('reciver')),sender_user=self.request.user.salesexecutive) 
        get.massage = self.request.user.salesexecutive.name +' '+ self.request.user.salesexecutive.typeExecutive + " send a massage"
        get.is_FirstTime = True
        get.save()
        messages.success(request,'massage send successfully')
        return redirect('/sales/Sendmassage')

def GetFeedbackesLeadWiseUsingAjexView(request):
    feedbackes = FeedBack.objects.filter(lead=request.GET.get('Selected_lead_id')).order_by('-typeFeedBack').values()
    return JsonResponse(list(feedbackes),safe=False)

def GetMyAssignedLeadsView(request):
    assignedLeadss = Lead.objects.filter(feeback_lead__nextCall=request.user.salesexecutive).order_by('-feeback_lead__time')
    return render(request,'sales/AssignedLeads.html',{'assignedLeadss':assignedLeadss})

def MessagesInboxView(request):
    Allmassages = Massages.objects.filter(reciverId=request.user.salesexecutive).order_by('-datetime')
    unread_massage_length = Allmassages.filter(massagRead=False).count()
    Notification.objects.filter(notification_user=request.user.salesexecutive).delete()
    context = {'usermassages':Allmassages,'unread_massage_length':unread_massage_length}
    return render(request,'sales/MessagesInbox.html',context)

def GetSpecificUserMessageView(request,user_id):
    specific_user_massages = Massages.objects.filter(reciverId=request.user.salesexecutive,senderId=user_id).order_by('-datetime')
    specific_user_massages.update(massagRead=True)
    return render(request,'sales/SpecificMessagesInbox.html',{'specific_user_massages':specific_user_massages})

def GetFeedbackesAndDemos_A_SpecificLeadWiseView(request):
    lead_id = request.GET['lead_id']
    feedbackes_SpecificLeadWise = FeedBack.objects.filter(lead=lead_id).order_by('-time')
    demos_SpecificLeadWise = DemoFeedback.objects.filter(lead=lead_id).order_by('-datetime')
    context = {'feedbackes_SpecificLeadWise':feedbackes_SpecificLeadWise,'demos_SpecificLeadWise':demos_SpecificLeadWise}
    return render(request,'sales/AllFeedbackAndDemo_A_SpecificLead.html',context)

def GetSpecificLeadAndFeedbackView(request,lead_id=None,feedback_id=None):
    specific_lead_and_feedback = Lead.objects.filter(id=lead_id).prefetch_related(
        Prefetch(
            "feeback_lead",
            queryset=FeedBack.objects.filter(id=feedback_id),
            to_attr="recieved_feedback"
        )
    )
    return render(request,'sales/SpecificLeadAndFeedback.html',{'specific_lead_and_feedback':specific_lead_and_feedback})
    
def logoutview(request):
    auth.logout(request)
    messages.success(request, 'Logged Out Successfully')
    return redirect('/sales/login')
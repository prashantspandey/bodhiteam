from django.shortcuts import render,redirect
from membership.models import SalesExecutive,TechPerson
from django.contrib import messages
from sales.models import *
from datetime import datetime, timezone
from django.db.models import Prefetch
from django.db.models import Q
# Create your views here.

def IndexView(request):
    if request.user.is_authenticated:
        try:
            request.user.salesexecutive 
            # getting lengths of all activities 
            currentUser = SalesExecutive.objects.filter(executiveUser=request.user.id).prefetch_related('lead_assign')
            new_leads_length = currentUser[0].lead_assign.filter(lead_status='is_successfull_lead').count()
            worked_leads_length = currentUser[0].lead_assign.filter(lead_status='worked_lead').count()
            allmessagelength = currentUser[0].reciever.filter(massagRead=False).count()
            allNotificationslength = currentUser[0].demofeedbackuser_notification.count()
            successfully_leads_length = currentUser[0].successfull_lead_user.count()
            assignedleads = Lead.objects.filter(Q(Q(feeback_lead__nextCall=request.user.salesexecutive) | Q(demo_lead__demo_nextCall=request.user.salesexecutive)) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))).count()
            
            # here we are check notifications of feedback & demo or messages 
            user_notification = Notification.objects.filter(notification_user=request.user.salesexecutive,is_FirstTime=True)    
            IsDemo_Or_feedback_schedule = DemoFeedback_And_LeadFeedback_Notifications.objects.filter(notification_user=request.user.salesexecutive,is_FirstTime=True)
            for i in IsDemo_Or_feedback_schedule:
                if str(i.nextDate).split(' ')[0] == str(datetime.now()).split(' ')[0]:
                    messages.info(request,i.massage)
                    i.is_FirstTime = False
                    i.save()
            context = {'user_notification':user_notification,'assignedleads':assignedleads,'allmessagelength':allmessagelength,'allNotificationslength':allNotificationslength,'NewleadsLenght':new_leads_length,'WorkedLeadsLenght':worked_leads_length,'successfully_leads_length':successfully_leads_length}
            return render(request,'Index.html',context)
        except:
            try:
                request.user.techperson
                return render(request,'Index.html')
            except:
                messages.error(request, 'Inside Only sales or teck user allowed ..and you are not a sales or teck user')
                return redirect('/sales/login')
    else:
        return redirect('/sales/login')
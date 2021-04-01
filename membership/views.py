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
            try:
                currentUser = SalesExecutive.objects.filter(executiveUser=request.user.id).prefetch_related(Prefetch("lead_assign",queryset=Lead.objects.filter(assignedTo=request.user.salesexecutive),to_attr="recieved_leads"))
                Newleads_list,WorkedLeads_list = [],[]
                for i in currentUser[0].recieved_leads:
                    if not i.feeback_lead.filter(lead=i.id).exists():
                        Newleads_list.append(i.id)
                    else:
                        WorkedLeads_list.append(i.id)
                allmessagelength = currentUser[0].reciever.filter(massagRead=False).count()
                allNotificationslength = currentUser[0].demofeedbackuser_notification.count()  
                assignedleads = Lead.objects.filter(Q(feeback_lead__nextCall=request.user.salesexecutive) | Q(demo_lead__demo_nextCall=request.user.salesexecutive)).count()
            except Exception as e:
                pass
    
            user_notification = Notification.objects.filter(notification_user=request.user.salesexecutive,is_FirstTime=True)
            IsDemo_Or_feedback_schedule = DemoFeedback_And_LeadFeedback_Notifications.objects.filter(notification_user=request.user.salesexecutive,is_FirstTime=True)
            for i in IsDemo_Or_feedback_schedule:
                try:
                    gapbeetwendates = i.nextDate - datetime.now(timezone.utc)  
                    if len(str(gapbeetwendates).split(',')) == 2:
                        if str(gapbeetwendates).split(',')[0] == str(datetime.now()).split(' ')[0]:
                            messages.warning(request,i.massage)
                            i.is_FirstTime = False
                            i.save()
                        else:
                            # print('no need to show notification')
                            pass
                    else:
                        messages.warning(request,i.massage)
                        i.is_FirstTime=False
                        i.save()
                except Exception as e:
                    pass
            context = {'user_notification':user_notification,'assignedleads':assignedleads,'allmessagelength':allmessagelength,
            'allNotificationslength':allNotificationslength,'NewleadsLenght':Newleads_list,'WorkedLeadsLenght':WorkedLeads_list}
            return render(request,'Index.html',context)
        except:
            try:
                request.user.techperson
                return render(request,'Index.html')
            except:
                messages.success(request, 'Inside Only sales or teck user allowed ..and you are not a sales or teck user')
                return redirect('/sales/login')
    else:
        return redirect('/sales/login')
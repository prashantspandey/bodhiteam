from django.shortcuts import render,redirect
from membership.models import SalesExecutive,TechPerson
from django.contrib import messages
from sales.models import *
from datetime import datetime, timezone
# Create your views here.

def IndexView(request):
    if request.user.is_authenticated:
        try:
            request.user.salesexecutive 
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
from rest_framework.views import APIView
from django.contrib.auth.models import User,Group
from rest_framework.response import Response
from sales.models import *
from membership.models import *
from tech.models import *
import datetime
from django.db.models import Prefetch
from .serializers import *

class GetMyNewLeads(APIView):
    def get(self,request):
        leads = Lead.objects.filter(assignedTo=self.request.user.salesexecutive).order_by('-date')
        leads_list = []
        for lead in leads:
            if not lead.feeback_lead.filter(lead=lead.id).exists():
                leads_list.append(lead)
        serializer = LeadSerializer(leads_list,many=True)
        context = {'Leads':serializer.data}
        return Response(context)

class GetMyNewLeadsDateWise(APIView):
    def post(self,request,*args,**kwargs):
        my_profile = self.request.user.salesexecutive
        data = request.data
        date= data['date']
        date = str(date.split('.')[0])
        date = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
        main_date = date.date()
        leads = Lead.objects.filter(assignedTo =my_profile,date__date=main_date).order_by('-date')
        leads_list = []
        for lead in leads:
            lead_dict =\
            {'name':lead.personName,'instituteName':lead.instituteName,'contactPhone':lead.contactPhone,'email':lead.email,'numberStudents':lead.numberStudents,'location':lead.location,'notes':lead.notes,'source':lead.source,'assignedTo':lead.assignedTo.name}
            leads_list.append(lead_dict)
        context = {'leads':leads_list,'date':str(main_date)}
        return Response(context)

class GiveLeadFeedBack(APIView):
    def post(self,request,*args,**kwargs):
        my_profile = self.request.user.salesexecutive
        data = request.data
        feedback = data['feedback']
        lead_id = data['lead_id']
        notes = data['notes']
        demo = data['demo']
        typeFeedBack = data['typeFeedBack']
        priceQuoted = data['priceQuoted']
        executiveId = data['nextCall']
        furtherCall = data['furtherCall']
        nextCallDate = data['nextCallDate']
        demoDate = data['demoDate']
        rating = data['rating']

        if nextCallDate == 'None':
            nextCallDate = None
        if demoDate == 'None':
            demoDate = None
        if demo == 'true':
            demo = True
        else:
            demo = False
        if furtherCall == 'true':
            furtherCall = True
        else:
            furtherCall = False
        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            return Response('Incorrect lead id ')

        feedback = FeedBack()
        feedback.by = my_profile
        feedback.typeFeedBack = typeFeedBack
        feedback.lead = lead
        feedback.rating = rating
        feedback.notes = notes
        feedback.Cource = data['cource']
        feedback.instituteType = data['instituteType']
        feedback.State = data['State']
        feedback.city = data['city']
        if data['Is_wrongLead'] == 'false':
            feedback.Is_wrongLead = False
        else:
            feedback.Is_wrongLead = True
        feedback.demo = demo
        feedback.demoDate = demoDate
        feedback.feedback = feedback
        feedback.furtherCall = furtherCall
        feedback.priceQuoted = priceQuoted
        if executiveId == 'None':
            feedback.nextCall = None
        else:
            NextCallerUser = SalesExecutive.objects.get(id=executiveId)
            feedback.nextCall = NextCallerUser
            DemoFeedback_And_LeadFeedback_Notifications.objects.create(notification_user=NextCallerUser,
            sender_user=my_profile,notification_type='LeadFeedbackNotification',lead=lead,
            massage = f"Today is your Feedback schedule of this {lead.personName} lead So remember This", is_FirstTime=True ,nextDate=nextCallDate)
        feedback.nextCallDate = nextCallDate
        feedback.save()
        context = {'status':'Saved','message':'Feedback saved'}
        return Response(context)

class FindTypeFeedBack(APIView):
    def post(self,request,*args,**kwargs):
        my_profile = self.request.user.salesexecutive
        data = request.data
        lead_id = data['lead_id']
        lead = Lead.objects.get(id=lead_id)
        feedback = FeedBack.objects.filter(lead=lead)
        feedback_length = len(feedback)
        typeFeedBack = feedback_length + 1
        context = {'typeFeedback':typeFeedBack}
        return Response(context)

class GetAllSalesExecutives(APIView):
    def get(self,request):
        sales_people = SalesExecutive.objects.all()
        sales_list = []
        for sp in sales_people:
            sp_dict = {'id':sp.id,'name':sp.name}
            sales_list.append(sp_dict)
        context = {'salesPeople':sales_list}
        return Response(context)

class GetWorkedLeadsApi(APIView):
    def get(self,request):
        leads = Lead.objects.filter(assignedTo=self.request.user.salesexecutive).order_by('-date')
        leads_list = []
        for lead in leads:
            if lead.feeback_lead.filter(lead=lead.id).exists():
                leads_list.append(lead)
        serializer = LeadSerializer(leads_list,many=True)
        context = {'Leads':serializer.data}
        return Response(context)

class GetFeedbackOrDemos_A_specificLeadWiseApi(APIView):
    def post(self,request,*args,**kwargs):
        lead_id = request.data['lead_id']
        feedbackes = FeedBack.objects.filter(lead=lead_id)
        demos = DemoFeedback.objects.filter(lead=lead_id)
        feedbackserializer = FeedBackSerializer(feedbackes,many=True)
        demosserializer = DemoFeedbackSerializer(demos,many=True)
        context = {'feedbacks': feedbackserializer.data,'demosfeedbackes':demosserializer.data}
        return Response(context)

class GiveDemoFeedBackApi(APIView):
    def post(self,request):
        data = request.data
        lead_id = data['lead_id']
        my_profile = self.request.user.salesexecutive
        lead = Lead.objects.get(id=lead_id)
        DemoNextUser = data['demo_nextCall']
        DemoNextDate = data['demo_nextCallDate']
        demofeedback = DemoFeedback(typedemo=DemoFeedback.objects.filter(lead=lead_id).count()+1, by=my_profile, lead=lead,
                                    datetime=datetime.datetime.now(),
                                    demo_rating=data['demo_rating'],
                                    extra_notes=data['extra_notes'],
                                    demo_feedback=data['demo_feedback'],
                                    price_quoted=data['price_quoted'])
        if DemoNextDate == 'None':
            demofeedback.demo_nextCallDate = None
            DemoNextDate = None
        else:
            demofeedback.demo_nextCallDate = DemoNextDate
        if DemoNextUser == 'None':
            demofeedback.demo_nextCall = None
        else:
            nextcaller = SalesExecutive.objects.get(id=DemoNextUser)
            demofeedback.demo_nextCall = nextcaller
            DemoFeedback_And_LeadFeedback_Notifications.objects.create(notification_user=nextcaller,sender_user=my_profile,notification_type='DemoNotification',lead=lead,
            massage = f"Today is your Demo schedule of this {lead.personName} lead So remember This",is_FirstTime = True,nextDate=DemoNextDate)
        demofeedback.save()
        return Response({'status':'Saved','message':'Demo saved'})

class GetMyAssignedLeadsAPI(APIView):
    def get(self,request):
        assignedLeadss = Lead.objects.filter(feeback_lead__nextCall=self.request.user.salesexecutive).order_by('-feeback_lead__time')
        serializer = LeadSerializer(assignedLeadss,many=True)
        return Response(serializer.data)    
        
class GetSpecificLeadAndFeedbackAPI(APIView):
    def post(self,request):
        feedback_id = request.data['feedback_id']
        if feedback_id == 'None':
            feedback_id = None
        specific_lead= Lead.objects.get(id=request.data['lead_id'])
        leadserializer = LeadSerializer(specific_lead)
        try:
            specific_feedback = FeedBack.objects.get(id=feedback_id)
            feedbackserializer =  FeedBackSerializer(specific_feedback)
            context = {'lead':leadserializer.data,'feedback':feedbackserializer.data}
            return Response(context)
        except FeedBack.DoesNotExist:
            return Response({'lead':leadserializer.data})
        
class SendMessageToUserAPI(APIView):
    def get(self,request):
        leads = None
        users = SalesExecutive.objects.prefetch_related('lead_assign').all()
        for i in users:
            if i.lead_assign.filter(assignedTo=self.request.user.salesexecutive).exists():
                leads = i.lead_assign.filter(assignedTo=self.request.user.salesexecutive).order_by('-date')
                break
        serializer = LeadSerializer(leads,many=True)
        Userserializer = SalesExecutiveSerializer(users,many=True)
        context = {'AllUsers':Userserializer.data,'leads':serializer.data}
        return Response(context)
    
    def post(self,request):
        data = request.data
        lead_id = data['lead_id']
        Lead_Feedback_Id = data['feedback_id']

        if Lead_Feedback_Id == 'None':
            Lead_Feedback_Id = None
        else:
            Lead_Feedback_Id = FeedBack.objects.get(id=Lead_Feedback_Id) 
        if lead_id == 'None':
            lead_id = None
        else:
            lead_id = Lead.objects.get(id=lead_id)

        Massages.objects.create(senderId=self.request.user.salesexecutive,reciverId=SalesExecutive.objects.get(id=data['reciver']),lead=lead_id,feedback=Lead_Feedback_Id,massage=data['message'],datetime=datetime.datetime.now())
        
        get,create = Notification.objects.get_or_create(notification_user=SalesExecutive.objects.get(id=data['reciver']),sender_user=self.request.user.salesexecutive) 
        get.massage = self.request.user.salesexecutive.name +' '+ self.request.user.salesexecutive.typeExecutive + " send a massage"
        get.is_FirstTime = True
        get.save()
        return Response('Message send successfully')

class GetFeedbackesLeadWiseUsingAjexAPI(APIView):
    def get(self,request):
        feedbackes = FeedBack.objects.filter(lead=request.data['Selected_Lead_id']).order_by('-typeFeedBack')
        feedbackserializer =  FeedBackSerializer(feedbackes,many=True)
        return Response({'feedbackes':feedbackserializer.data})

class MessagesInboxAPI(APIView):
    def get(self,request):
        Allmassages = Massages.objects.filter(reciverId=self.request.user.salesexecutive).order_by('-datetime')
        unread_message_length = Allmassages.filter(massagRead=False).count()
        Notification.objects.filter(notification_user=self.request.user.salesexecutive).delete()
        messageserializer =  MassagesSerializer(Allmassages,many=True)
        context = {'UserAllMessages':messageserializer.data,'unread_message_length':unread_message_length}
        return Response(context)

class GetMySpecificMessageAPI(APIView):
    def post(self,request): 
        specific_user_massages = Massages.objects.filter(reciverId=self.request.user.salesexecutive,senderId=request.data['user_id']).order_by('-datetime')
        specific_user_massages.update(massagRead=True)
        messageserializer =  MassagesSerializer(specific_user_massages,many=True)
        return Response({'messgaes':messageserializer.data})

class LogoutUserApi(APIView):
    def get(self,request):
        try:
            self.request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return Response('Logout successfully')
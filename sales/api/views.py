from rest_framework.views import APIView
from django.contrib.auth.models import User,Group
from rest_framework.response import Response
from sales.models import *
from membership.models import *
from tech.models import *
import datetime


class GetMyNewLeads(APIView):
    def get(self,request):
        my_profile = self.request.user.salesexecutive
        leads = Lead.objects.filter(assignedTo=my_profile).order_by('-date')
        leads_list = []
        for lead in leads:
            lead_dict =\
                    {'id':lead.id,'name':lead.personName,'instituteName':lead.instituteName,'contactPhone':lead.contactPhone,'email':lead.email,'numberStudents':lead.numberStudents,'location':lead.location,'notes':lead.notes,'source':lead.source,'assignedTo':lead.assignedTo.name}
            leads_list.append(lead_dict)
        context = {'leads':leads_list}
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
        executiveId = data['executiveId']
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

        executive = SalesExecutive.objects.get(id=executiveId)
        lead = Lead.objects.get(id=lead_id)

        feedback = FeedBack()
        feedback.by = my_profile
        feedback.typeFeedBack = typeFeedBack
        feedback.lead = lead
        feedback.rating = rating
        feedback.notes = notes
        feedback.demo = demo
        feedback.demoDate = demoDate
        feedback.feedback = feedback
        feedback.furtherCall = furtherCall
        feedback.priceQuoted = priceQuoted
        feedback.nextCall = executive
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

class GetWorkedLeads(APIView):
    def get(self,request):
        leads = Lead.objects.filter(assignedTo=self.request.user.salesexecutive).prefetch_related('feeback_lead').order_by('-date')
        leads_list = []
        for lead in leads:
            if lead.feeback_lead.filter(lead=lead.id).exists():
                leads_dict = {'lead_id': lead.id, 'PersonName': lead.personName, 'InstituteName': lead.instituteName,
                              'Date': lead.date, 'ContactPhone': lead.contactPhone,
                              'email': lead.email, 'NumberStudents': lead.numberStudents, 'location': lead.location,
                              'notes': lead.notes, 'source': lead.source, 'assignedTo': str(lead.assignedTo)}
                leads_list.append(leads_dict)
            else:
                pass
        context = {'Leads':leads_list}
        return Response(context)

class GetSpecificFeedbackOrDemos(APIView):
    def post(self,request,*args,**kwargs):
        lead_id = request.data['lead_id']
        feedback = FeedBack.objects.filter(lead=lead_id)
        feedback_list = []
        for feedback in feedback:
            feedback_dict = {'typeFeedBack':feedback.typeFeedBack,'by':str(feedback.by),'lead':str(feedback.lead),'time':feedback.time,
                             'rating':feedback.rating,'notes':feedback.notes,'nextCall':str(feedback.nextCall),'nextCallDate':feedback.nextCallDate,
                             'demo':feedback.demo,'demoDate':feedback.demoDate,'feedback':feedback.feedback,'furtherCall':feedback.furtherCall,'priceQuoted':feedback.priceQuoted}
            feedback_list.append(feedback_dict)

        demos_list = []
        try:
            demos = DemoFeedback.objects.filter(lead=lead_id)
            for demo in demos:
                demo_dict = {'typedemo':demo.typedemo,'by':str(demo.by),'lead':str(demo.lead),'demo_rating':demo.demo_rating,
                              'demo_feedback':demo.demo_feedback,'extra_notes':demo.extra_notes,'price_quoted':demo.price_quoted,
                              'datetime':demo.datetime,'demo_nextCall':str(demo.demo_nextCall),'demo_nextCallDate':demo.demo_nextCallDate}
                demos_list.append(demo_dict)
            context = {'feedbacks':feedback_list,'demos':demos_list}
            return Response(context)
        except DemoFeedback.DoesNotExist:
            context = {'feedbacks': feedback_list,'demos':demos_list}
            return Response(context)

class GiveDemoFeedBack(APIView):
    def post(self,request):
        lead_id = request.data['lead_id']
        my_profile = self.request.user.salesexecutive
        lead = Lead.objects.get(id=lead_id)
        demofeedback = DemoFeedback(typedemo=request.data['typedemo'], by=my_profile, lead=lead,
                                    datetime=datetime.datetime.now(),
                                    demo_rating=request.data['demo_rating'],
                                    extra_notes=request.data['extra_notes'],
                                    demo_feedback=request.data['demo_feedback'],
                                    price_quoted=request.data['price_quoted'])
        if request.data['demo_nextCall'] == None:
            demofeedback.demo_nextCall = SalesExecutive.objects.get(id=request.data['demo_nextCall'])
        else:
            demofeedback.demo_nextCall = None

        if request.data['demo_nextCallDate'] == None:
            demofeedback.demo_nextCallDate = request.data['demo_nextCallDate']
        else:
            demofeedback.demo_nextCallDate = None
        demofeedback.save()
        return Response({'status':'Saved','message':'Demo saved'})

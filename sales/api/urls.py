from django.conf.urls import url
from django.urls import path
from sales.api import views



urlpatterns = [
    url(r'get_my_leads/$',views.GetMyNewLeads.as_view(),name='salesExecutiveGetLeads'),
    url(r'get_my_datewise_leads/$',views.GetMyNewLeadsDateWise.as_view(),name='salesExecutiveGetDateWiseLeads'),
    url(r'give_feedback_lead/$',views.GiveLeadFeedBack.as_view(),name='giveLeadFeedBack'),
    url(r'find_type_feedback/$',views.FindTypeFeedBack.as_view(),name='findTypeFeedBack'),
    url(r'get_all_sales_people/$',views.GetAllSalesExecutives.as_view(),name='getAllSalesExecutive'),
    url(r'get_my_worked_leads/$', views.GetWorkedLeads.as_view(), name='get_my_all_leads'),
    url(r'get_specific_feedback_or_demos/$', views.GetSpecificFeedbackOrDemos.as_view(), name='get_specific_feedback_or_demos'),
    url(r'give_demo_feedback/$', views.GiveDemoFeedBack.as_view(), name='give_demo_feedback'),

]

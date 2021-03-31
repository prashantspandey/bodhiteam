from django.urls import path
from django.conf.urls import url
from . import views
app_name = 'sales'

urlpatterns = [
    path('upload_csv',views.lead_upload,name='uploadLoad'),
    path('login',views.loginView,name='login'),
    path('logout',views.logoutview,name='logout'),
    path('Get_my_new_leads',views.GetMyNewLeadView,name='Get_my_all_leads'),
    path('Get_my_worked_leads',views.GetMyWorkedLeadsView,name='Get_my_worked_leads'),
    path('GetFeedbackesAsnDemos_Specificlead_wise/',views.GetFeedbackesAndDemos_A_SpecificLeadWiseView,name='GetMyFeedbackesLeadWise'),
    url(r'feedback_creating/$',views.FeedbackCreateView.as_view(),name='feedback'),
    url(r'demo_creating/$',views.DemoCreatingView.as_view(),name='demo_creating'),
    url(r'Sendmassage/$',views.SendMassageToUserView.as_view(),name='Sendmassage'),
    url(r'add_comfirmLead/$',views.AddSuccessfullyLeadView.as_view(),name='add_comfirmLead'),
    path('getting_feedbackes_leadwise_by_ajex/',views.GetFeedbackesLeadWiseUsingAjexView,name='getting_feedbackes_leadwise_by_ajex'),
    path('messagesInbox/',views.MessagesInboxView,name='messagesInbox'),
    path('Get_specific_user_messages/<int:user_id>/',views.GetSpecificUserMessageView,name='Get_specific_user_messages'),
    path('Get_specific_lead_andfeedback/<int:lead_id>/',views.GetSpecificLeadAndFeedbackView,name='Get_specific_lead_andfeedback'),
    path('Get_specific_lead_andfeedback/<int:lead_id>/<int:feedback_id>/',views.GetSpecificLeadAndFeedbackView,name='Get_specific_lead_andfeedback'),
    path('Get_my_assigned_leads/',views.GetMyAssignedLeadsView,name='Get_my_assigned_leads'),
    path('Get_my_all_notifications/',views.GetMyAllNotificationsView,name='Get_my_all_notifications'),
    path('Specific_person_successfullLeads/',views.SpecificPersonSuccessfullyLeadsView,name='Specific_person_successfullLeads'),

]

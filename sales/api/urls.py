from django.conf.urls import url
from django.urls import path
from sales.api import views



urlpatterns = [
    url(r'get_my_New_leads/$',views.GetMyNewLeads.as_view(),name='salesExecutiveGetLeads'),
    url(r'get_my_datewise_leads/$',views.GetMyNewLeadsDateWise.as_view(),name='salesExecutiveGetDateWiseLeads'),
    url(r'give_feedback_lead/$',views.GiveLeadFeedBack.as_view(),name='giveLeadFeedBack'),
    url(r'find_type_feedback/$',views.FindTypeFeedBack.as_view(),name='findTypeFeedBack'),
    url(r'get_all_sales_people/$',views.GetAllSalesExecutives.as_view(),name='getAllSalesExecutive'),
    
    url(r'get_my_worked_leads/$', views.GetWorkedLeadsApi.as_view(), name='get_my_all_leads'),
    url(r'get_feedback_or_demos_A_specificLead/$', views.GetFeedbackOrDemos_A_specificLeadWiseApi.as_view(), name='get_specific_feedback_or_demos'),
    url(r'give_demo_feedback/$', views.GiveDemoFeedBackApi.as_view(), name='give_demo_feedback'),
    url(r'Get_MyAssignedLeads/$', views.GetMyAssignedLeadsAPI.as_view(), name='Get_MyAssignedLeads'),
    url(r'Get_specific_lead_andfeedback/$', views.GetSpecificLeadAndFeedbackAPI.as_view(), name='Get_specific_lead_andfeedback'),
    url(r'Send_message_to_user/$', views.SendMessageToUserAPI.as_view(), name='Send_message_to_user'),
    url(r'Get_feedbackes_leadwise_by_ajex/$', views.GetFeedbackesLeadWiseUsingAjexAPI.as_view(), name='Get_feedbackes_leadwise_by_ajex'),
    url(r'Get_my_all_message/$', views.MessagesInboxAPI.as_view(), name='Get_my_all_message'),
    url(r'Get_specific_massages/$', views.GetMySpecificMessageAPI.as_view(), name='Get_specific_massages'),
    url(r'specific_user_notifications/$', views.SpecificUserNotificationsAPI.as_view(), name='specific_user_notifications'),
    url(r'add_successfull_lead/$', views.AddSuccessfullyLeadsAPI.as_view(), name='add_successfull_lead'),
    url(r'get_my_successfully_leads/$', views.SpecificPersonSuccessfullyLeadsAPI.as_view(), name='get_my_successfully_leads'),
    url(r'applyFilterAndSearch/$', views.ApplyFilterAndSeacrhAPI.as_view(), name='applyFilterAndSearch'),
    url(r'applysorting/$', views.SortingApplyAPI.as_view(), name='applysorting'),
    url(r'salesUserProfile/$', views.SalesUserProfileApi.as_view(), name='salesUserProfile'),
    url(r'salesUser_changePassword/$', views.SalesUserChangePasswordApi.as_view(), name='salesUser_changePassword'),
    url(r'filterAndSortForAdmin/$', views.FilterAndSortForAdminApi.as_view(), name='filterAndSortForAdmin'),
    url(r'assignLeadToAnotherUser/$', views.AssignLeadToAnotherUserApi.as_view(), name='assignLeadToAnotherUser'),
    url(r'deleteLead/$', views.DeleteLeadByAdminApi.as_view(), name='deleteLead'),

    url(r'logout/$', views.LogoutUserApi.as_view(), name='logout'),

]

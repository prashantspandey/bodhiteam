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
    path('Get_my_feedbackes_lead_wise/<int:lead_id>/',views.GetMyFeedbackesLeadWise,name='GetMyFeedbackesLeadWise'),
    url(r'feedback/$',views.FeedbackCreateView.as_view(),name='feedback'),
    url(r'demo_creating/$',views.DemoCreatingView.as_view(),name='demo_creating'),
]

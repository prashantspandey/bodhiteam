from django.contrib import admin
from .models import *
# Register your models here.

class LeadAdmin(admin.ModelAdmin):
    search_fields = ("personName","email")
    list_filter = ('date','source','assignedTo')
    list_display = ("personName","assignedTo","email","contactPhone",)

class FeedBackAdmin(admin.ModelAdmin):
    search_fields = ("typeFeedBack",)
    list_filter = ('time','by','lead')
    list_display = ("typeFeedBack","by","lead","rating","demo")

class DemoFeedbackAdmin(admin.ModelAdmin):
    search_fields = ("typedemo","demo_rating")
    list_filter = ('datetime','by','lead')
    list_display = ("typedemo","by","lead","demo_rating","demo_feedback")

class MassagesAdmin(admin.ModelAdmin):
    list_filter = ('datetime','senderId',)

class DemoFeedback_And_LeadFeedback_NotificationsAdmin(admin.ModelAdmin):
    list_display = ('notification_user','sender_user','lead','nextDate')
    list_filter = ('datetime','nextDate','notification_user')
    
admin.site.register(Lead,LeadAdmin)
admin.site.register(FeedBack,FeedBackAdmin)
admin.site.register(DemoFeedback,DemoFeedbackAdmin)
admin.site.register(Massages,MassagesAdmin)
admin.site.register(Notification)
admin.site.register(SuccessfullyLead)
admin.site.register(DemoFeedback_And_LeadFeedback_Notifications,DemoFeedback_And_LeadFeedback_NotificationsAdmin)

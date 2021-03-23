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

admin.site.register(Lead,LeadAdmin)
admin.site.register(FeedBack,FeedBackAdmin)
admin.site.register(DemoFeedback,DemoFeedbackAdmin)
admin.site.register(Massages,MassagesAdmin)
admin.site.register(Notification)

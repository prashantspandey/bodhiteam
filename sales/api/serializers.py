from rest_framework import serializers
from sales.models import *
from membership.models import SalesExecutive

class LeadSerializer(serializers.ModelSerializer):
    assignedTo = serializers.SerializerMethodField()
    def get_assignedTo(self, obj):
        return str(obj.assignedTo)
    class Meta:
        model = Lead
        fields = '__all__'

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = '__all__'

class DemoFeedbackSerializer(serializers.ModelSerializer):
    by = serializers.SerializerMethodField()
    def get_by(self, obj):
        return str(obj.by)
            
    class Meta:
        model = DemoFeedback
        fields = '__all__'

class SalesExecutiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesExecutive
        fields = ['executiveUser','name','photo','joiningDate','typeExecutive']

class MassagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Massages
        fields = '__all__'

class DemoFeedback_And_LeadFeedback_NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoFeedback_And_LeadFeedback_Notifications
        fields = '__all__'

class SuccessfullyLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessfullyLead
        fields = '__all__'


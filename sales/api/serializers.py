from rest_framework import serializers
from sales.models import *
from membership.models import SalesExecutive

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = '__all__'

class DemoFeedbackSerializer(serializers.ModelSerializer):
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
from django.contrib import admin
from membership.models import *
# Register your models here.

class SalesExecutiveAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ('joiningDate','typeExecutive')
    list_display = ("name","typeExecutive","joiningDate")

admin.site.register(SalesExecutive,SalesExecutiveAdmin)
admin.site.register(TechPerson)
admin.site.register(Technology)



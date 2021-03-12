from django.shortcuts import render
import csv, io
import pandas as pd
from .models import *
from django.http import HttpResponse
# Create your views here.


def lead_upload(request):
    template = 'sales/lead_upload.html'
    if request.method == 'GET':
        return render(request,template,{})
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'This is not csv')
    df = pd.read_csv(csv_file)
    final_list = []
    sources = df['Source']
    notes = df['Notes']
    name = df['Client Name']
    phone = df['Phone Number']
    email = df['Email']
    final_list = list(zip(sources,name,phone,email,notes))
    for so,na,ph,em,no in final_list:
        lead = Lead.objects.filter(contactPhone=ph)
        if len(lead) > 0:
            continue
        else:
            number_students = 0
            type_educatior = ''
            details = no.split('\n')
            for det in details:
                if 'Educator' in det:
                    type_educator = det.split(':')[1]
                if 'Students' in det:
                    number_students = det.split(':')[1]
            leads =\
            Lead(personName=na,source=so,contactPhone=ph,email=em,numberStudents=number_students,notes=type_educator)
            leads.save()
    #data_set = csv_file.read().decode('UTF-8')
    #io_string = io.StringIO(data_set)
    #next(io_string)
    #for column in csv.reader(io_string,delimiter=',',quotechar="|"):
    #    print('type column {}'.format(type(column)))
    #    for col in column:
    #        print(col)
    #    #print('source {}'.format(column[0]))
    #    #print('whatsapp number {}'.format(column[1]))
    #    #print('display name {}'.format(column[2]))
    #    #print('date {}'.format(column[3]))
    #    #print('name {}'.format(column[4]))
    #    #print('notes {}'.format(column[6]))
    context = {}
    return render(request,template,context)


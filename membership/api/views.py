from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from membership.models import *
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login


class Login(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        username = data['username']
        password = data['password']
        typeUser = data['typeUser']
        try:
            user = authenticate(username=username,password=password)
            #django_login(request,user)
            token,created = Token.objects.get_or_create(user=user)
            if typeUser == 'sales':
                finalUser = SalesExecutive.objects.get(executiveUser=user)
            elif typeUser == 'tech':
                finalUser = TechPerson.objects.get(executiveUser=user)
            context =\
                    {'status':'Success','token':token.key,'username':username,'name':finalUser.name,'typeUser':typeUser}
        except Exception as e:
            context = {'status':'Failed','message':str(e)}
        return Response(context)

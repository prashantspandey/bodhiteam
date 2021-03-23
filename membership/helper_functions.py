from membership.models import *
class SalesPerson:
    def __init__(self,user):
        self.profile = user.salesexecutive
        self.name = self.profile.name

class TechGuy:
    def __init__(self,user):
        self.profile = user.techperson

def CheckUserType(id):
    teck = TechPerson.objects.get(executiveUser=id)
    sales = SalesExecutive.objects.filter(executiveUser=id)
    return teck


    
                



from django.db import models
from greenadmin.models import GreenAdmin 
from person.models import GreenUser 
 

class Supplier(models.Model):
    person = models.OneToOneField(GreenUser, on_delete=models.CASCADE, related_name="persons")
    admin = models.ForeignKey(GreenAdmin, on_delete=models.CASCADE, related_name="suppliers")



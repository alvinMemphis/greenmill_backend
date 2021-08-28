from django.db import models
from greenadmin.models import GreenAdmin 
from person.models import GreenUser 
 

class Supplier(models.Model):
    person = models.OneToOneField(GreenUser, on_delete=models.CASCADE, related_name="persons")
    admin = models.ForeignKey(GreenAdmin, on_delete=models.CASCADE, related_name="suppliers")



class Package(models.Model):
    ORDER_TYPE_STATUS = (
     ('confirmed', 'confirmed'),
     ('shipped', 'shipped'),
     ('out for delivery', 'out for delivery'),
     ('delivered', 'delivered'),
    )

    packagename = models.CharField(max_length=100)
    supplier = models.ForeignKey(GreenUser, on_delete=models.CASCADE, related_name="customersuppliers", default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    orderstat = models.CharField(max_length=40,choices=ORDER_TYPE_STATUS, default='confirmed')
    to_customer_name =  models.CharField(max_length=100)
    to_customer_email =  models.CharField(max_length=100)

    def __str__(self):
        return self.packagename

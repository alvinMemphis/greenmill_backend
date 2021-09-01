from django.db import models
from hubmanager.models import HubManager, LogicHub
from person.models import GreenUser 
 

# Create your models here.

class HubLoader(models.Model):
    user = models.OneToOneField(GreenUser, on_delete=models.CASCADE, related_name="greenloaders")
    manager = models.ForeignKey(HubManager, on_delete=models.CASCADE, related_name="hmanagers")
    his_hub = models.ForeignKey(LogicHub, on_delete=models.CASCADE, null=True, related_name="hubs", default=1)
    
    def __str__(self):
        return "Loader: " + self.user.user_name
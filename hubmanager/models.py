from django.db import models
from greenadmin.models import GreenAdmin 
from person.models import GreenUser 
 

class HubManager(models.Model):
    user = models.OneToOneField(GreenUser, on_delete=models.CASCADE, related_name="greenusers")
    admin = models.ForeignKey(GreenAdmin, on_delete=models.CASCADE, related_name="managers")

    def __str__(self):
        return "Manager: " + self.user.user_name

class LogicHub(models.Model):
    hubname = models.CharField(max_length=100)
    hubowner = models.ForeignKey(GreenAdmin, on_delete=models.CASCADE, related_name="hubowners", default='1', null=True)
    hubmanager = models.ForeignKey(HubManager, on_delete=models.CASCADE,null=True, related_name="hubmanagers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hubname
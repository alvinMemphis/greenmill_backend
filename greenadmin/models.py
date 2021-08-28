from django.db import models
from person.models import GreenUser
# from hubmanager.models import HubManager as q


# Create your models here.
class GreenAdmin(models.Model):
    user = models.OneToOneField(GreenUser, on_delete=models.CASCADE, related_name='user_admin')

# class LogicHub(models.Model):
#     hubname = models.CharField(max_length=100)
#     hubowner = models.ForeignKey(GreenAdmin, on_delete=models.CASCADE, related_name="hubowners", default='1', null=True)
#     # hubmanager = models.ForeignKey(HubManager, on_delete=models.CASCADE,null=True, related_name="hubmanagers")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.hubname
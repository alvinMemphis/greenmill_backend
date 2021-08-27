from django.db import models
from person.models import GreenUser

# Create your models here.
class GreenAdmin(models.Model):
    user = models.OneToOneField(GreenUser, on_delete=models.CASCADE, related_name='user_admin')
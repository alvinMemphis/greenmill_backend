from django.contrib import admin
from .models import HubManager
# Register your models here.


@admin.register(HubManager)
class HubManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)

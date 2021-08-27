from django.contrib import admin
from person.models import GreenUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models

'''

A fix to: 
    Can't delete users if using token blacklist app

'''
from rest_framework_simplejwt.token_blacklist import models
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin

class NewOutstandingTokenAdmin(OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True # default is False in the blacklist admin

admin.site.unregister(models.OutstandingToken)
admin.site.register(models.OutstandingToken, NewOutstandingTokenAdmin)
'''
 
 End of fix:

'''




class UserAdminConfig(UserAdmin):
    model = GreenUser
    search_fields = ('email', 'user_name',)
    list_filter = ('email', 'user_name', 'start_date', 'is_active', 'is_staff')
    readonly_fields = ('id', 'start_date')
    ordering = ('-start_date',)
    list_display = ('id', 'email', 'user_name', 'start_date',
                    'is_active', 'is_staff')

    fieldsets = ()
    # exclude = ['username']
    # fieldsets = (
    #     (None, {'fields': ('email', 'user_name',)}),
    #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
    #     ('Personal', {'fields': ('about',)}),
    # )
    # formfield_overrides = {
    #     models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    # }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_verified', 'user_type')}
         ),
    )


admin.site.register(GreenUser, UserAdminConfig)
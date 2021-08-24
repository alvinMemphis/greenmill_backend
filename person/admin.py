from django.contrib import admin
from person.models import GreenUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models


class UserAdminConfig(UserAdmin):
    model = GreenUser
    search_fields = ('email', 'user_name',)
    list_filter = ('email', 'user_name', 'start_date', 'is_active', 'is_staff')
    readonly_fields = ('id', 'start_date')
    ordering = ('-start_date',)
    list_display = ('id', 'email', 'user_name', 'start_date',
                    'is_active', 'is_staff')

    fieldsets = ()
    # fieldsets = (
    #     (None, {'fields': ('email', 'user_name',)}),
    #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
    #     ('Personal', {'fields': ('about',)}),
    # )
    # formfield_overrides = {
    #     models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    # }
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'user_name', 'password1', 'password2', 'is_active', 'is_staff')}
    #      ),
    # )


admin.site.register(GreenUser, UserAdminConfig)
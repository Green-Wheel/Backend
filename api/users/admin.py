from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.users.models import Users, Languages, LoginMethods


class LanguagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortname')
    search_fields = ('name', 'shortname')

class LoginMethodsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register your models here.
admin.site.register(Users, UserAdmin)
admin.site.register(Languages, LanguagesAdmin)
admin.site.register(LoginMethods, LoginMethodsAdmin)

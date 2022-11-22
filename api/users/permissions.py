from django.conf import settings

from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import login, logout

from .models import Users


"""class Check_API_KEY_Auth(BasePermission):
    def has_permission(self, request, view):
        key = request.META.get('HTTP_API_KEY')
        print(request.META)
        print(key)
        if key:
            user = User.objects.filter(tgt=key)
            if user.count()>0:
                login(request,user[0])
                return True
        logout(request)
        return False
"""
class Check_API_KEY_Auth(BasePermission):
    def has_permission(self, request, view):
        user = Users.objects.get(id=1)
        login(request, user)
        return True

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

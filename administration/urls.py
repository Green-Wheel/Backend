"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('solve/<int:report_id>/',views.solve_report,name="solve_report"),
    path('users/', views.users, name="gestio_usuaris"),
    path('users/<int:user_id>/', views.change_user,name="change_user"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.signout, name="logout"),
]

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
    path("", views.VehiclesView.as_view()),
    path("<int:car_id>/", views.DetailedVehicleView.as_view()),
    path("brands/", views.BrandsView.as_view()),
    path("brands/<int:brand_id>/models", views.ModelsBrandView.as_view()),
    path("brands/<int:brand_id>/models/<str:model_name>/years", views.ModelsBrandYearView.as_view()),
    path("<int:car_id>/select/", views.SelectVehicleView.as_view()),
]

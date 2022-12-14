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
    path('', views.UserApiView.as_view()),
    path('<int:user_id>/', views.ConcreteUserApiView.as_view()),
    path('language/', views.LanguageApiView.as_view()),
    path('<int:user_id>/posts/', views.UserPostsApiView.as_view()),
    path('register/', views.RegisterApiView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('logout/', views.LogoutApiView.as_view()),
    path('password/recovery/', views.RecoverPasswordApiView.as_view()),
    path('password/change/', views.ChangePasswordApiView.as_view()),
    path('upload/', views.UploadProfileImageApiView.as_view()),
    path('login/google/', views.GoogleLoginCallbackApiView.as_view()),
    path('login/raco/', views.RacoLoginCallbackApiView.as_view()),
    path('<int:user_id>/notifications/', views.SendNotificationTest.as_view()),
]

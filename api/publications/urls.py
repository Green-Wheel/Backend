from django.urls import path
from . import views

urlpatterns = [
    path("<int:publication_id>/upload/", views.UploadPublicationImageApiView.as_view()),
]

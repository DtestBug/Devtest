from django.urls import path
from .views import Project

urlpatterns = [
    path('project/', Project.as_view()),
    path('project/<int:pk>', Project.as_view()),
]

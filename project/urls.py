from django.urls import path
from .views import Project,Projects

urlpatterns = [
    #http://127.0.0.1:8000/index/project/
    path('project/', Project.as_view()),
    path('project/<int:pk>', Project.as_view()),

    #http://127.0.0.1:8000/index/projects/多条数据get使用
    path('projects/', Projects.as_view())
]

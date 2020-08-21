from django.urls import path
from project import views

urlpatterns = [

    # a.继承ViewSet之后，支持在定义路由时指定请求方法与action的映射
    # b.as_view需要接收一个字典
    # c.key为请求方法名，value为指定需要调用的action
    path('projects/<int:pk>', views.ProjectsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

    path('projects/', views.ProjectsViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),

    path('projects/names/', views.ProjectsViewSet.as_view({
        'get': 'names'
    })),

    path('projects/<int:pk>/interfaces', views.ProjectsViewSet.as_view({
        'get': 'retrieve'
    }))
]

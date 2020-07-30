from django.contrib import admin
from django.urls import path
from .views import Interface,Interfaces

urlpatterns = [
    path('interface/<int:pk>', Interface.as_view()),#GET接口-查询指定数据
    path('interface/', Interface.as_view()),#传数据接口-查询所有数据

    path('interfaces/', Interfaces.as_view()),  # GET接口-查询所有数据
]
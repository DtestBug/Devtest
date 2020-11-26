from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import ReportsModelSerializer
from .models import Reports
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action  # 导入装饰器


class ReportsViewSet(mixins.ListModelMixin,  # 查询list
                     mixins.RetrieveModelMixin,  # 查询单个
                     mixins.DestroyModelMixin,  # 删除数据
                     GenericViewSet):  # 必须继承

    queryset = Reports.objects.all()  # 查询集
    serializer_class = ReportsModelSerializer  # 序列化
    permission_classes = [permissions.IsAuthenticated]  # 用户权限
    ordering_fields = ['id', 'name']

    def retrieve(self, request, *args, **kwargs):
        pass

from rest_framework.viewsets import ModelViewSet
from .serializers import TestCasesModelSerializer
from .models import Testcases
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action  # 导入装饰器


class TestCasesViewSet(ModelViewSet):
    queryset = Testcases.objects.all()  # 查询集
    serializer_class = TestCasesModelSerializer  # 序列化
    permission_classes = [permissions.IsAuthenticated]  # 用户权限
    ordering_fields = ['id', 'name']  #

    @action(detail=False)
    def names(self, request, *args, **kwargs):
        qs = self.get_queryset()
        return Response(self.get_serializer(qs, many=True).data)
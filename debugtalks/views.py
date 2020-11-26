from rest_framework.viewsets import ModelViewSet
from .serializers import DebugtalksModelSerializer
from .models import Debugtalks
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action  # 导入装饰器


class DebugtalksViewSet(ModelViewSet):
    queryset = Debugtalks.objects.all()  # 查询集
    serializer_class = DebugtalksModelSerializer  # 序列化
    permission_classes = [permissions.IsAuthenticated]  # 用户权限
    ordering_fields = ['id', 'project_id']  #

    @action(detail=False)
    def names(self, request, *args, **kwargs):
        qs = self.get_queryset()
        return Response(self.get_serializer(qs, many=True).data)
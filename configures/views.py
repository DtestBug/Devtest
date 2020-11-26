from rest_framework.viewsets import ModelViewSet
from .serializers import ConfiguresModelSerializer
from .models import Configures
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action  # 导入装饰器


class ConfiguresViewSet(ModelViewSet):
    queryset = Configures.objects.all()  # 查询集
    serializer_class = ConfiguresModelSerializer  # 序列化
    permission_classes = [permissions.IsAuthenticated]  # 用户权限
    ordering_fields = ['id', 'name']  #

    @action(detail=False)
    def names(self, request, *args, **kwargs):
        qs = self.get_queryset()
        return Response(self.get_serializer(qs, many=True).data)

    # def get_serializer_class(self):
    #     '''
    #     if self.action == 'names':
    #         return EnvsNamesSerializer
    #     else:
    #         return self.permission_classes
    #     '''
    #     return ConfiguresNamesSerializer if self.action == 'names' else self.serializer_class  # 三元运算
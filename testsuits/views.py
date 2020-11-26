from rest_framework.viewsets import ModelViewSet
from .serializers import TestsuitsModelSerializer
from .models import Testsuits
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action  # 导入装饰器


class TestsuitsViewSet(ModelViewSet):
    queryset = Testsuits.objects.all()  # 查询集
    serializer_class = TestsuitsModelSerializer  # 序列化
    permission_classes = [permissions.IsAuthenticated]  # 用户权限
    ordering_fields = ['id', 'name']  #

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            'name': instance.name,
            'project_id': instance.project_id,
            'include': instance.include
        }
        return Response(data)

    # @action(detail=False)
    # def names(self, request, *args, **kwargs):
    #     qs = self.get_queryset()
    #     return Response(self.get_serializer(qs, many=True).data)

    # def get_serializer_class(self):
    #     '''
    #     if self.action == 'names':
    #         return EnvsNamesSerializer
    #     else:
    #         return self.permission_classes
    #     '''
    #     return TestsuitsModelSerializer if self.action == 'names' else self.serializer_class  # 三元运算

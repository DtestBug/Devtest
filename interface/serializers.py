from rest_framework import serializers
from rest_framework import validators
from .models import Interface_Mo
from project.models import Project_Mo
# from project.serializers import ProjectModelSerializer


class InterfaceModelSerializer(serializers.ModelSerializer):#类名自定义
    # email = serializers.EmailField(write_only=True)
    # project = serializers.PrimaryKeyRelatedField(help_text='所属项目', label='所属项目', queryset=Project_Mo.objects.all())

    # ============单字段显示=============
    # 返回父表项目id对应的值///projects命名是固定的，少了s之后无法显示
    # 会将父表对应对象的__str__方法结果返回
    projects = serializers.StringRelatedField()
    # projects = serializers.SlugRelatedField(slug_field='desc', read_only=True)

    # ============多字段显示=============
    # 数据按照project项目内的序列化器定义为字段规则来的
    # projects = ProjectModelSerializer(label='所属项目信息', help_text='所属项目信息', read_only=True)

    class Meta:
        model = Interface_Mo
        fields = '__all__'

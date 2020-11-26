from rest_framework import serializers
from rest_framework import validators

from .models import Testsuits
from project.models import Project_Mo
from interface.models import Interface_Mo
from utils.common import datetime_fmt
import re


def validate_include(value):  # include自定义校验方法
    obj = re.match(r'\[\d+(,\d+)*\]$', value)
    if obj is None:
        raise serializers.ValidationError('参数格式有误,列表内应为数字')
    else:
        res = obj.group()
        try:
            data = eval(res)

        except:
            raise serializers.ValidationError('参数格式有误,列表内应为数字')

        for item in eval(res):
            if not Interface_Mo.objects.filter(id=item).exists():
                raise serializers.ValidationError(f'接口id不存在【{item}】不存在')


class TestsuitsModelSerializer(serializers.ModelSerializer):  # 类名自定义
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
                                                    queryset=Project_Mo.objects.all(), write_only=True)

    class Meta:
        model = Testsuits
        fields = ('id', 'name', 'project', 'project_id', 'include', 'create_time', 'update_time')

        extra_kwargs = {
            'create_time': {
                'format': datetime_fmt()
            },
            'update_time': {
                'format': datetime_fmt()
            },
            'include': {
                'write_only': True,
                'validators': [validate_include]  # 自定义校验方法，传入的值非列表有提示
            }
        }

    def create(self, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
            return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
            # instance 为旧数据，validated_data为新上传数据
            return super().update(instance, validated_data)

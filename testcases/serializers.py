from project.models import Project_Mo
from rest_framework import serializers
from interface.models import Interface_Mo
from testcases.models import Testcases
from utils import common, validates
# 需要输入的字段（docs接口输入，前端输入）
"""
==== 需要输入 ====
project: 项目
pid: 项目id
iid: 接口id

label: docs内的输入标签, 必须加
help_text: 同上
write_only: 必须输入数据
validators: 校验规则, 导入了其他文件的校验方法，可以自定义
"""


class InterfacesProjectsModelSerializer(serializers.ModelSerializer):  # 类名自定义
    project = serializers.StringRelatedField(label='所属项目', help_text='所属项目')
    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id', write_only=True,
                                   validators=[validates.is_existed_project_id])
    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id', write_only=True,
                                   validators=[validates.is_existed_interface_id])

    # 需要输出接口返回，展示的数据
    class Meta:
        model = Interface_Mo
        fields = ('name', 'pid', 'iid')

    # 输出(展示)格式
    def validate(self, attrs):
        pid = attrs.get('pid')  # attrs.get: 已输入pid
        iid = attrs.get('iid')  # attrs.get: 已输入iid
        if not Interface_Mo.objects.filter(id=iid, project_id=pid).exists():
            raise serializers.ValidationError('所属项目id与接口id不匹配')


"""
TestCasesModelSerializer类
需要输入interface，也就是InterfacesProjectsModelSerializer类的内容
"""


class TestCasesModelSerializer(serializers.ModelSerializer):  # 类名自定义
    interface = InterfacesProjectsModelSerializer(label='所属项目和接口', help_text='所属项目和接口')

    """
    输出内容
    required: 必须传值
    exclude: 不输出
    write_only: 只写入
    """
    class Meta:
        model = Testcases
        exclude = ('update_time', 'create_time')

        extra_kwargs = {
            'request': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        iid = validated_data.pop('interface').get('iid')
        validated_data['interface_id'] = iid
        return super().create(validated_data)
# 48:05  十七（1）

from rest_framework import serializers
from project.models import Project_Mo
from interface.models import Interface_Mo
"""
校验函数
1.以下方法在serializers内调用的时候不需要加括号()
"""


# 判断id是否存在
def is_existed_project_id(value):
    """
    校验接口id是否存在
    :param value:
    :return:
    """
    if not Project_Mo.objects.all(id=value).exists():  # 如果输入的value（id）不存在
        raise serializers.ValidationError('项目id不存在')  # 抛出异常提示项目id不存在


def is_existed_interface_id(value):
    """
    校验接口id是否存在
    :param value:
    :return:
    """
    if not Interface_Mo.objects.all(id=value).exists():  # 如果输入的value（id）不存在
        raise serializers.ValidationError('接口id不存在')  # 抛出异常提示接口id不存在

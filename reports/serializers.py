from rest_framework import serializers
from rest_framework import validators

from reports.models import Reports
from utils import common


class ReportsModelSerializer(serializers.ModelSerializer):  # 类名自定义

    class Meta:
        model = Reports
        exclude = ('update_time', )  # 不需要输出

        # 输出校验
        extra_kwargs = {
            'create_time': {
                'format': common.datetime_fmt()  # 创建时间输出格式为此函数
            },
            'html': {
                'write_only': True
            },
        }

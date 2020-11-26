from rest_framework import serializers
from rest_framework import validators

from envs.models import Envs
from utils import common


class EnvsModelSerializer(serializers.ModelSerializer):  # 类名自定义

    class Meta:
        model = Envs
        exclude = ('update_time', )

        extra_kwargs = {
            'create_time': {
                'read_only': False,
                'format': common.datetime_fmt(),
            },
        }


class EnvsNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Envs
        fields = ('id', 'name')

        # extra_kwargs = {
        #     'create_time': {
        #         'read_only': False,
        #         'format': common.datetime_fmt(),
        #     },
        # }

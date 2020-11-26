from rest_framework import serializers
from rest_framework import validators

from debugtalks.models import Debugtalks
from utils import common


class DebugtalksModelSerializer(serializers.ModelSerializer):  # 类名自定义

    class Meta:
        model = Debugtalks
        # fields = '__all__'
        fields = ('id', 'name', 'debugtalk')

from rest_framework import serializers
from rest_framework import validators

from configures.models import Configures
from utils import common


class ConfiguresModelSerializer(serializers.ModelSerializer):  # 类名自定义

    class Meta:
        model = Configures
        fields = '__all__'

from rest_framework import serializers
from rest_framework import validators

from testcases.models import Testcases
from utils import common


class TestcasesModelSerializer(serializers.ModelSerializer):  # 类名自定义

    class Meta:
        model = Testcases
        fields = '__all__'

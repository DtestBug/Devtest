from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User  # django自带的user方法
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

class RegisterSerializer(serializers.ModelSerializer):  # 类名自定义
    password_confirm = serializers.CharField(label='确认密码', help_text='确认密码',
                                             min_length=6,
                                             max_length=20,
                                             write_only=True,
                                             error_messages={
                                                 'min_length': '密码最小长度为6个字符',
                                                 'max_length': '密码最大长度为20个字符'
                                                }
                                             )
    token = serializers.CharField(label='生成token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'password_confirm', 'token')
        extra_kwargs = {
            'username': {
                'label': '用户名',
                'help_text': '用户名',
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '用户名最小长度为6个字符',
                    'max_length': '用户名最大长度为20个字符'
                                    }
                        },

            'email': {
                'label': '邮箱',
                'help_text': '邮箱',
                'write_only': True,
                'required': True,

                'validators': [UniqueValidator(queryset=User.objects.all(), message='此邮箱已注册')]
                     },

            'password': {
                'label': '密码',
                'help_text': '密码',
                'write_only': True,
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '密码最小长度为6个字符',
                    'max_length': '密码最大长度为20个字符'
                                    }
                        }
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError('密码与确认密码不一致')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        # 创建user模型对象
        user = User.objects.create(**validated_data)

        # 创建token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token
        return user









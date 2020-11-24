from rest_framework import serializers
from rest_framework import validators
from .models import Interface_Mo
from project.models import Project_Mo
# from project.serializers import ProjectModelSerializer

# class InterfaceSerializer(serializers.Serializer):
#     """
#     可以定义序列化器类，来实现序列化和反序列化操作
#     a.一定要继承serializers.Serializer
#     b.默认情况下，可以定义序列化器字段，序列化器字段名一定要与模型类中字段名相同
#     c.默认情况下，定义几个序列化器字段，那么就会返回几个数据到前端,序列化输出的过程，前端也必须得传递这几个字段，反序列化过程
#     d.CharField，BooleanField,IntegerField与模型类中的字段类型一一对应
#     e.required参数默认为None,指定前端必须得传此字段，如果设置为False的话，前端可以不传此字段
#     f.lable和help_text————》》verbose_name和help_text一一对应
#     g.allow_null指定前端传递参数时可以传空值
#     CharField字段，max_length指定该字段不能操作的字节参数
#     """
#     id = serializers.CharField(max_length=20,label='id',help_text='id',required=False)
#     name = serializers.CharField(max_length=200,label='项目名称', help_text='项目名称',
#                                  validators=[validators.UniqueValidator(queryset=Interface_Mo.objects.all(),message='项目已存在')],allow_blank=False)
#     # leader = serializers.CharField(max_length=200,label='项目负责人', help_text='项目负责人')
#     # h.如果某个字段指定read_only=Ture,那么此字段，前端在创建数据时（反序列化过程）可以不用传，但是一定会输出
#     # i.字段不能同时指定read_only=Ture，required=True
#     # k.字段不能同时指定write_only=Ture,read_only=Ture
#     # l.可以给字段添加error_messages参数，为字典类型，字典的key为校验的参数名，值为校验失败之后错误提示
#     # leader = serializers.CharField(max_length=200,label='项目负责人', help_text='项目负责人')#,read_only=True
#     # tester = serializers.CharField(max_length=200,label='测试人员', help_text='测试人员')
#     # 如果某个字段指定write_only=True,那么此字段只能进行反序列化输入，而不会输出（创建数据时必须传，但是数据不返回）
#     # tester = serializers.CharField(max_length=200,label='测试人员', help_text='测试人员')#,write_only=True,error_messages={"required":'该字段为必填项'}
#     projects_id = serializers.CharField(max_length=50,label='所属项目',help_text='所属项目')
#     tester = serializers.CharField(max_length=50,label='测试人员',help_text='测试人员')
#     desc = serializers.CharField(max_length=200,label='简要描述',help_text='简要描述')
#
#     def validate_name(self, value):
#         if '非常' in value:
#             raise serializers.ValidationError('项目名称中不能包含"非常"')
#         return value
#
#     def validate(self, attrs):
#         if len(attrs['name']) != 8 or '测试' not in attrs['tester']:
#             raise serializers.ValidationError('项目名长度不为8或者测试人员名称中不包含"测试"')
#         return attrs
#
#     def create(self, validated_data):
#         obj = Interface_Mo.objects.create(**validated_data)
#         return obj
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name') or instance.name
#         instance.tester = validated_data.get('leader') or instance.tester
#         instance.projects_id = validated_data.get('projects_id') or instance.projects_id
#         instance.desc = validated_data.get('desc') or instance.desc
#         instance.save()
#         return instance

class InterfaceModelSerializer(serializers.ModelSerializer):#类名自定义
    # email = serializers.EmailField(write_only=True)

    #这行代码在上传数据的时候可以关联父表id，如果注释后是无法上传和更新数据的。同时父表查询返回的是原有name信息
    # projects = serializers.PrimaryKeyRelatedField(help_text='所属项目', label='所属项目', queryset=Project_Mo.objects.all(),error_messages={"required":'该字段为必填项'})

    # ============单字段显示=============
    # 返回父表项目id对应的值///projects命名是固定的，少了s之后无法显示
    # 会将父表对应对象的__str__方法结果返回
    # projects = serializers.StringRelatedField()
    # projects = serializers.SlugRelatedField(slug_field='desc', read_only=True)

    # ============多字段显示=============多字段名字可以随机命名，单字段规定与models内一致
    # 数据按照project项目内的序列化器定义为字段规则来的
    # project = ProjectModelSerializer(label='所属项目信息', help_text='所属项目信息', read_only=True)

    class Meta:
        model = Interface_Mo
        fields = '__all__'

    # def create(self, validated_data):
        # email = validated_data.pop('email')
        # return super().create(validated_data)

    # def create(self, validated_data):
    #     Interface_Mo(name='', projects_id=1)
    #     return super().create(validated_data)




























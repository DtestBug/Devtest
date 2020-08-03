from rest_framework import serializers
from rest_framework import validators
from .models import Project_Mo
from interface.serializers import InterfaceModelSerializer

#前端待校验的值自动传送给value
# def is_name_contain_x(value):
#     if 'x' in value:
#         raise serializers.ValidationError('项目名称中不能包含x')
#     return value

# serializers.Serializer序列化
class ProjectSerializer(serializers.Serializer):
    """
    可以定义序列化器类，来实现序列化和反序列化操作
    a.一定要继承serializers.Serializer
    b.默认情况下，可以定义序列化器字段，序列化器字段名一定要与模型类中字段名相同
    c.默认情况下，定义几个序列化器字段，那么就会返回几个数据到前端,序列化输出的过程，前端也必须得传递这几个字段，反序列化过程
    d.CharField，BooleanField,IntegerField与模型类中的字段类型一一对应

    e.required参数默认为None,指定前端必须得传此字段，如果设置为False的话，前端可以不传此字段
    f.lable和help_text————》》verbose_name和help_text一一对应
    g.allow_null指定前端传递参数时可以传空值
    CharField字段，max_length指定该字段不能操作的字节参数
    """
    # id = serializers.CharField(max_length=20,label='id',help_text='id')
    # name = serializers.CharField(max_length=200,label='项目名称', help_text='项目名称')
    # leader = serializers.CharField(max_length=200,label='项目负责人', help_text='项目负责人')
    # h.如果某个字段指定read_only=Ture,那么此字段，前端在创建数据时（反序列化过程）可以不用传，但是一定会输出
    # i.字段不能同时指定read_only=Ture，required=True
    # k.字段不能同时指定write_only=Ture,read_only=Ture
    # l.可以给字段添加error_messages参数，为字典类型，字典的key为校验的参数名，值为校验失败之后错误提示
    # leader = serializers.CharField(max_length=200,label='项目负责人', help_text='项目负责人')#,read_only=True
    # tester = serializers.CharField(max_length=200,label='测试人员', help_text='测试人员')
    # 如果某个字段指定write_only=True,那么此字段只能进行反序列化输入，而不会输出（创建数据时必须传，但是数据不返回）
    # tester = serializers.CharField(max_length=200,label='测试人员', help_text='测试人员')#,write_only=True,error_messages={"required":'该字段为必填项'}
    # projects_id = serializers.CharField(max_length=50,label='项目名称',help_text='所属项目')
    # tester = serializers.CharField(max_length=50,label='项目名称',help_text='测试人员')
    # desc = serializers.CharField(max_length=200,label='项目名称',help_text='简要描述')

    id = serializers.CharField(max_length=20,label='id',help_text='id',required=False)
    name = serializers.CharField(max_length=10,label='项目名称',help_text='项目名称',
                                 validators=[validators.UniqueValidator(queryset=Project_Mo.objects.all())],allow_blank=False)
    leader = serializers.CharField(max_length=50,label='leader',help_text='项目负责人',allow_blank=False)
    tester = serializers.CharField(max_length=50,label='tester',help_text='测试人员')
    programmer = serializers.CharField(max_length=50,label='programmer',help_text='开发人员',allow_blank=False)
    desc = serializers.CharField(help_text='项目简介',label='desc',max_length=50,allow_blank=False,)
    create_time = serializers.DateTimeField(help_text='创建时间',label='create_time',required=False)
    update = serializers.DateTimeField(help_text='创建时间',label='upd',required=False)


    #在序列化器类中对单字段进行校验
    # 必须要以validate_作为前缀
    # 校验方法名称为：validate_字段名（例如：validate_name)字段名不能错误
    # c.一定要返回校验之后的值
    def validate_name(self, value):
        if '非常' in value:
            raise serializers.ValidationError("项目名称中不能包含'非常'")
        return value

    #在序列化器类中对多字段进行联合校验统一用validate
    #一定要把校验后的值返回前端
    def validate(self, attrs):
        if len(attrs['name']) < 8 or '测试' not in attrs['tester']:
            raise serializers.ValidationError('项目名长度不为8或者测试人员名称中不包含"测试"')
        return attrs

    def create(self, validated_data):
        obj=Project_Mo.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id') or instance.id
        instance.name = validated_data.get('name') or instance.name
        instance.leader = validated_data.get('leader') or instance.leader
        instance.tester = validated_data.get('tester') or instance.tester
        instance.programmer = validated_data.get('programmer') or instance.programmer
        instance.desc = validated_data.get('desc') or instance.desc
        instance.save()
        return instance


#使用模型序列化器类：简化序列化器类中字段的创建
# a:需要继承ModelSerializer

class ProjectModelSerializer(serializers.ModelSerializer):#类名自定义

    email = serializers.EmailField(write_only=True)


    #interface的projects_id为几，这个id就是project内的id下的全部数据
    #如果模型类modles.py中外键字段定义了related_name参数，那么会使用这个名称作为字段名，就不需要加_set了
    interface_mo_set = InterfaceModelSerializer(label='所拥有的接口', many=True)

    # interface的projects_id为几，这个id就是project内的id下的name字段
    # interface_mo_set = serializers.StringRelatedField(many=True)

    # 一、validators.UniqueValidator内
    # 1.queryset=Project_Mo.objects.all()全部查询集
    # 2.message='项目名重复'自定义返回的报错

    # 二、validators.UniqueValidator外
    # 1.max_length最大长度
    # 2.min_length最小长度
    # 3.allow_blank是否允许为空
    # 4.trim_whitespace是否截断空白字符
    # 5.max_value最大值
    # 6.min_value最小值
    # 7.read_only表明该字段仅用于序列化输出，默认False
    # 8.write_only表明该字段仅用于反序列化输入，默认False
    # 9.required表明该字段在反序列化时必须输入，默认True
    # 10.default反序列化时使用的默认值
    # 11.allow_null表明该字段是否允许传入None，默认False
    # 12.validators该字段使用的验证器
    # 13.error_messages包含错误编号与错误信息的字典
    # 14.lable用于HTML展示API页面时，显示的字段名称
    # 15.help_text用于HTML展示API页面时，显示的字段帮助提示信息
    # =========================================================

    # 如果再模型序列化器类中显示指定了模型类中的某个字段，那么会将models内自动生成的字段覆盖掉
    # name = serializers.CharField(max_length=10,label='项目名称',help_text='项目名称',
    #                              validators=[validators.UniqueValidator(queryset=Project_Mo.objects.all())],allow_blank=False)

    # 以下类名与变量为固定名字
    class Meta:
        # a:需要再Meta内部类这两个指定model类属性；需要按照哪一个模型来创建
        # b:fields类属性来指定，模型类中哪些字段需要输入或者输出
        # c:默认id主键，会添加read_only=True
        # d:create_time和update_time，会添加read_only=True

        model = Project_Mo

        # 视图类内的请求体内必须要有这个类才可以触发以下条件
        # ===========================================================================================
        # fields和exclude只能用一个，否则会报AssertionError: You must call `.is_valid()` before accessing `.errors`.的错误
        # 生成所有的序列化器字段，__all__包含models数据库内所有的字段
        fields = '__all__'
        # fields = ("id","name","leader","tester","interface_mo_set","programmer","desc","email")

        # 生成指定的序列化器字段，以下字段名必须为models内的字段名
        # fields = ('id', 'name', 'leader', 'tester', 'programmer')

        # models所有字段中需要排除的一项添加到exclude内,
        # 不展示到前端,但是数据可以保存到数据库
        # exclude = ('create_time', 'update_time',)
        # ============================================================================================
        # 只输出不输入.
        # 上传的时候忽略read_only_fields内传的字段post和put上传的数据无法传递到数据库和前端页面,
        # 如果数据库和前端有数据一定是定义模型时候默认的数据
        # 但是传参的时候必须传,否则会报错
        # read_only_fields = ('id', 'desc', )

        # 可以在extra_kwargs中定制字段或者新增字段，字段校验或重置使用extra_kwargs,校验方法写错会有波浪线
        extra_kwargs = {
            'name':{
                    'max_length': 10,
                    'min_length': 4,
                    'label': '项目名称',
                    'help_text': '项目名称',
                    'validators': [validators.UniqueValidator(queryset=Project_Mo.objects.all(), message='项目已存在')]
            },

            'programmer': {
                    'label': ' 研发人员',
                    'write_only': False,
                    'max_length': 10,
                    'min_length': 4
            },
                        }

    def create(self, validated_data):
        email = validated_data.pop('email')
        return super().create(validated_data)
        # return Project_Mo.objects.create(**validated_data)
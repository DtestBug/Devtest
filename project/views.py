from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse, Http404
from .models import Project_Mo
from interface.models import Interface_Mo
from django.db.models import Count
from .serializers import ProjectSerializer, ProjectModelSerializer, ProjectsNamesModelSerializer, \
    InterFacesByProjectIdModelSerializer, InterfacesNamesModelSerializer, InterFacesByProjectIdModelSerializer1
import json
# =========================
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from utils.pagination import MyPagination
from django.db.models import Count
import logging
from rest_framework import permissions  # 认证
from configures.models import Configures
from testsuits.models import Testsuits
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

logger = logging.getLogger("test")  # 日志器为settings.py中定义的日志器名

# POST与PUT上传数据时候需要注意项：
# 1.一定要先执行is_valid()方法之后才能访问,is_valid()目的是检测数据是否有效
# 2. .errors获取报错的信息
# 3. .validated_data校验通过之后的数据
# 4. .data最终必须要返回给前端的数据
ret1 = {
    'msg': '参数有误',
    'code': 10001,
}

ret2 = {'msg': '操作成功',
        'code': 10002,
        }


# 1.需要继承APIView
# a.对Django中的View进行了拓展
# b.具备认证/授权/限流/
# 2.需要使用drf中的Response返回需要的东西
# a.对Django中的HttpResponse进行了拓展
# b.实现了根据请求头张Accept参数来动态返回
# c.默认情况下，如果不传Accept参数或者创建applications/json，那么会返回json格式
# d.如果Accept参数text/html，那么会返回可浏览的api页面（html）

# 如果要实现过滤、查询、分页等功能，需要继承GenericAPIView
# a.GenericAPIView为APIview的子类，拓展了过滤、查询、分页


class XXXMinxin:
    def list(self, *args, **kwargs):
        lists = self.filter_queryset(self.get_queryset())  # 覆盖重写查询集lists
        page = self.paginate_queryset(lists)
        if page is not None:
            serializer_obj = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data)
        one = self.get_serializer(instance=lists, many=True)
        return Response(one.data, status=status.HTTP_200_OK)  # 1.status指定响应状态码


class Projects(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    # b.往往要指定queryset，当前接口中需要使用到的查询集（查询集对象）
    # c. 往往要指定serializer_class,当前接口中需要使用到的序列化器类
    queryset = Project_Mo.objects.all()  # 查询集
    serializer_class = ProjectModelSerializer  # 序列化器类
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # 过滤引擎,排序引擎
    filterset_fields = ['name', 'leader', 'id']  # 过滤字段
    ordering_fields = ['id', 'name']  # 排序引擎   示例：http://127.0.0.1:8000/index/projects/?ordering=id，id前面加-可以倒序
    pagination_class = MyPagination  # 在视图中指定分页

    # b. instance参数可以传查询集（多条记录），加上many=True
    # d.如果未传递many=True参数，那么序列化器对象.data返回的是字典，否则返回一个嵌套字典的列表
    def get(self, request, *args, **kwargs):
        # pro_obj = self.get_object()
        # one = self.get_serializer(instance=pro_obj)  # 查询单个数据的时候不能加many=True否则报错:TypeError: 'Project_Mo' object is not iterable
        # return Response(one.data, status=status.HTTP_200_OK)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        # request.query_params

        # 继承ApiView之后，request为Request
        # a.对Django中的HttpRequest进行了拓展
        # b.统一使用Request对象.data属性去获取json格式的参数，form表单参数，files
        # c.Django支持的参数获取方式，DRF都支持
        # .GET>>>查询字符串参数>>>.query_params
        # .POST>>>x-www-form-encoded
        # .body>>>获取请求体参数
        # d.Request对象.data属性为将请求数据转化为python中的字典（嵌套字典的列表）
        # res = self.get_serializer(data=request.data)
        # # try:
        # res.is_valid(raise_exception=True)
        # # except Exception as e:
        # #     ret1.update(res.errors)
        # #     return Response(ret1, status=status.HTTP_400_BAD_REQUEST)
        # res.save() # 使用序列化器对象.save()可以自动调用序列化器类中的create方法
        # return Response(res.data, status=status.HTTP_201_CREATED)


class Project(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    # b.往往要指定queryset，当前接口中需要使用到的查询集（查询集对象）
    # c. 往往要指定serializer_class,当前接口中需要使用到的序列化器类
    queryset = Project_Mo.objects.all()  # 查询集
    serializer_class = ProjectModelSerializer  # 序列化器类

    # filter_backends = [DjangoFilterBackend, OrderingFilter]  # 过滤引擎,排序引擎
    # filterset_fields = ['name', 'leader', 'id']  #过滤字段
    #
    # # 在ordering_fields来指定需要排序的字段
    # #  前端在过滤时，需要使用ordering作为key,具体的排序字段作为value
    # # 默认使用升序过滤，如果要降序，可以在排序字段前使用减号
    # ordering_fields = ['id', 'name']  # 排序引擎   示例：http://127.0.0.1:8000/index/projects/?ordering=id，id前面加-可以倒序
    # pagination_class = MyPagination  # 在视图中指定分页

    # 查询数据库所有数据
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        # JsonResponse转化数据为json格式
        # ProjectModelSerializer：serializers文件内的模型序列化类
        # Projects_Mo.objects.all():查询项目模型里所有的数据
        # instance参数可以传查询集（多条记录），加上many=True
        # 如果未传递many=True参数，那么序列化器对象
        # .data返回的是字典，否则返回一个嵌套字典的列表
        # safe=False：为了允许序列化非dict对象，请将safe参数设置为False
        # json_dumps_params={"ensure_ascii": False}
        # lists = Project_Mo.objects.all()

        # 尽量使用get_queryset()获取查询集对象，不直接使用self.queryset
        # 还有get_serializer获取序列化
        # lists = self.filter_queryset(self.get_queryset())  # 覆盖重写查询集lists
        # page = self.paginate_queryset(lists)
        # if page is not None:
        #     serializer_obj = self.get_serializer(instance=page, many=True)
        #     return self.get_paginated_response(serializer_obj.data)
        #
        # one = self.get_serializer(instance=lists, many=True)
        # # 1.status指定响应状态码
        # return Response(one.data,status=status.HTTP_200_OK)

        # 过滤需要安装第三方模块django-filter，还有再设置内的子应用注册django_filters,
        # 再导入过滤引擎：from django_filters.rest_framework import DjangoFilterBackend
        # pip install django - filter

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
        # pro_obj = self.get_object()
        # res = self.get_serializer(instance=pro_obj, data=request.data)  # instance传递的参数为查询出来的参数，data传递的参数为需要更新的参数,必须用sava来保存
        # # try:
        # res.is_valid(raise_exception=True)
        # # except Exception as e:
        # #     ret1.update(res.errors)
        # #     return Response(ret1, status=status.HTTP_400_BAD_REQUEST)
        # res.save() # save方法自动调用update
        # return Response(res.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        # pro_obj = self.get_object()
        # pro_obj.delete()
        # return Response(None, status=status.HTTP_204_NO_CONTENT)


# GenericAPIView和APIView只支持对get,post,put,delete,patch等请求方法
# 如果要支持action,需要继承ViewSet
# 当前ViewSet，无法支持.get_object()，.filter_queryset(),.paginate_queryset()
# class ProjectsViewSet(viewsets.ViewSet)
# GenericViewSet才支持对列表数据进行过滤，排序，分页操作
# class ProjectsViewSet(mixins.ListModelMixin,  # 列表查询
#                       mixins.RetrieveModelMixin,  # 单条查询
#                       mixins.CreateModelMixin,  # 创建数据
#                       mixins.UpdateModelMixin,  # 更新数据
#                       mixins.DestroyModelMixin,  # 删除数据
#                       viewsets.GenericViewSet):  #支持对列表数据进行过滤，排序，分页操作

# viewsets.ModelViewSet支持以上所有功能（查，建，改，删）

class ProjectsViewSet(viewsets.ModelViewSet):  # 支持对列表数据进行过滤，排序，分页操作

    # 以下内容均为接口文档内的操作描述
    """
    项目视图
    list:
        获取项目的列表信息
    create:
        创建新的项目
    names:
        查看项目名字
    read:
        读取项目详情
    update:
        更新数据
    partial_update:
        局部更新
    delete:
        删除数据
    interfaces:
        interfaces项目数据
    """

    queryset = Project_Mo.objects.all()  # 查询集
    serializer_class = ProjectModelSerializer  # 序列化器类，ProjectsNamesModelSerializer、ProjectModelSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]  # 过滤引擎,排序引擎
    # filterset_fields = ['name', 'leader', 'id']  #过滤字段
    # ordering_fields = ['id', 'name']  # 排序引擎   示例：http://127.0.0.1:8000/index/projects/?ordering=id，id前面加-可以倒序
    pagination_class = MyPagination  # 在视图中指定分页
    # authentication_classes = ['']  # authentication_classes在视图中指定权限，可以在列表中添加多个权限类
    # permission_classes = [permissions.IsAdminUser]  # 视图中指定的权限优先级大于全局指定的权限


    # 标记需要进行jwt验证
    authentication_classes = (JSONWebTokenAuthentication,)
    def list(self, request, *args, **kwargs):
        response = super().list(self, request, *args, **kwargs)
        results = response.data['results']
        data_list = []
        for item in results:
            # item 为一条项目数据所在的字典
            # 需要获取当前项目所属的接口总数用例总数，配置总数，套件总数
            project_id = item.get('id')
            # 1.使用.annotate()方法，那么会自动使用当前模型类的主键，作为分组条件
            # 2.使用.annotate()方法里可以添加聚合函数，计算的名称为从表名小写（还需要在外键字段上设置，related_name）
            # 3.values可以指定需要查询的字段（默认为所用字段）
            # 4.可以给聚合函数指定别名，默认为tesstcases_count
            # 5.如果values放在annotate前面，那么聚合运算的字段不需要再values中添加，放在后面需要
            interfaces_obj = Interface_Mo.objects.annotate(testcases1=Count('testcases')).values('id', 'testcases1').filter(project_id=project_id)
            interfaces_testcases_qs = Interface_Mo.objects.values('id').annotate(testcases=Count('testcases')).filter(project_id=project_id)

            # interfaces总数
            interfaces_count = interfaces_testcases_qs.count()

            # 用例总数
            testcases_count = 0
            for one_dict in interfaces_testcases_qs:
                testcases_count += one_dict.get('testcases')

            # 获取项目下的配置总数
            interfaces_configure_qs = Interface_Mo.objects.values('id').annotate(
                configures=Count('configures')).filter(project_id=project_id)
            configures_count = 0
            for one_dict in interfaces_configure_qs:
                configures_count += one_dict.get('configures')

            # 获取项目下的套件总数
            testsuits_count = Testsuits.objects.filter(project_id=project_id).count()

            item['interfaces'] = interfaces_count
            item['testcases'] = testcases_count
            item['testsuits'] = testsuits_count
            item['configures'] = configures_count
            data_list.append(item)
        response.data['results'] = data_list
        return response


    # 可以试用action装饰器去自定义动作方法
    # methods参数默认为['get']，可以定义支持请求方式['get', 'post', 'put']
    # detail参数为必传参数，指定是否为详情数据（如果需要传递主键ID，那么detail=True,否则为False）
    # 添加url_path指定url路径，不添加则默认为action名称(当前为names)
    # url_name指定url的名称，默认为action名称(当前names)

    @action(methods=['get'], detail=False)  # methods请求方式。  detail=True是详情数据，=False的时候是列表类型的数据# url_path='nnn'
    def names(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

    @action(detail=True)
    def interfaces(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectsNamesModelSerializer

        elif self.action == 'interfaces':
            # return InterFacesByProjectIdModelSerializer
            return InterFacesByProjectIdModelSerializer1
        else:
            return self.serializer_class

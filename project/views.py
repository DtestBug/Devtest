from django.shortcuts import render
from django.views import View
from django.http import JsonResponse,HttpResponse,Http404
from .models import Project_Mo
from .serializers import ProjectSerializer,ProjectModelSerializer
import json
# =========================
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


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
class Project(APIView):

    def get_object(self,pk):
        try:
            pro_obj = Project_Mo.objects.get(id=pk)
        except Exception as e:
            raise Http404('哦，我的上帝！您访问的页面飞到九霄云外咯。')
        return pro_obj


    # b. instance参数可以传查询集（多条记录），加上many=True
    # d.如果未传递many=True参数，那么序列化器对象.data返回的是字典，否则返回一个嵌套字典的列表

    def get(self,request, pk):
        pro_obj = self.get_object(pk)
        one = ProjectModelSerializer(instance=pro_obj)#查询单个数据的时候不能加many=True否则报错:TypeError: 'Project_Mo' object is not iterable
        # return JsonResponse(one.data,json_dumps_params={"ensure_ascii": False},safe=False)
        return Response(one.data, status=status.HTTP_200_OK)

    def post(self,request):
        # request.query_params

        # 继承ApiView之后，request为Request
        # a.对Django中的HttpRequest进行了拓展
        # b.统一使用Request对象.data属性去获取json格式的参数，form表单参数，files
        # c.Django支持的参数获取方式，DRF都支持
            # .GET>>>查询字符串参数>>>.query_params
            # .POST>>>x-www-form-encoded
            # .body>>>获取请求体参数
        # d.Request对象.data属性为将请求数据转化为python中的字典（嵌套字典的列表）
        res = ProjectModelSerializer(data=request.data)
        try:
            res.is_valid(raise_exception=True)
        except Exception as e:
            ret1.update(res.errors)
            return Response(ret1, status=status.HTTP_400_BAD_REQUEST)
        res.save() # 使用序列化器对象.save()可以自动调用序列化器类中的create方法
        return Response(res.data, status=status.HTTP_201_CREATED)

    def put(self,request, pk):
        pro_obj = self.get_object(pk)
        res = ProjectModelSerializer(instance=pro_obj, data=request.data) # instance传递的参数为查询出来的参数，data传递的参数为需要更新的参数,必须用sava来保存
        try:
            res.is_valid(raise_exception=True)
        except Exception as e:
            ret1.update(res.errors)
            return Response(ret1, status=status.HTTP_400_BAD_REQUEST)
        res.save() # save方法自动调用update
        return Response(res.data, status=status.HTTP_201_CREATED)

    def delete(self,request, pk):
        pro_obj = self.get_object(pk)
        pro_obj.delete()
        ret2['data'] = f'id:{pk}'
        # return JsonResponse(ret2)
        return Response(ret2, status=status.HTTP_204_NO_CONTENT)

class Projects(APIView):

    # 查询数据库所有数据
    def get(self,request):
        # JsonResponse转化数据为json格式
        # ProjectModelSerializer：serializers文件内的模型序列化类
        # Projects_Mo.objects.all():查询项目模型里所有的数据
        # instance参数可以传查询集（多条记录），加上many=True
        # 如果未传递many=True参数，那么序列化器对象
        # .data返回的是字典，否则返回一个嵌套字典的列表
        # safe=False：为了允许序列化非dict对象，请将safe参数设置为False
        # json_dumps_params={"ensure_ascii": False}
        lists = Project_Mo.objects.all()

        # 示例：http://127.0.0.1:8000/index/projects/?name=今天吃什么3
        name = request.query_params.get('name')
        if name is not None:
            lists = lists.filter(name=name)
        one = ProjectModelSerializer(instance=lists,many=True)
        # 1.status指定响应状态码
        return Response(one.data,status=status.HTTP_200_OK)









from django.shortcuts import render
from django.views import View
from django.http import JsonResponse,HttpResponse
from .models import Project_Mo
from .serializers import ProjectSerializer,ProjectModelSerializer
import json

# POST与PUT上传数据时候需要注意项：
# 1.一定要先执行is_valid()方法之后才能访问,is_valid()目的是检测数据是否有效
# 2. .errors获取报错的信息
# 3. .validated_data校验通过之后的数据
# 4. .data最终必须要返回给前端的数据

class Project(View):


    # def get(self,request):
    #     lists = Project_Mo.objects.all()
    #     one = ProjectSerializer(instance=lists,many=True)
    #     return JsonResponse(one.data,json_dumps_params={"ensure_ascii": False},safe=False)

    # b. instance参数可以传查询集（多条记录），加上many=True
    # d.如果未传递many=True参数，那么序列化器对象.data返回的是字典，否则返回一个嵌套字典的列表
    def get(self,request,pk=None):
        res = {}
        try:
            pro_obj = Project_Mo.objects.get(id=pk)
        except Exception as e:
            res['msg'] = '数据不存在'
            return JsonResponse(res,json_dumps_params={"ensure_ascii": False},)
        one = ProjectModelSerializer(instance=pro_obj)#查询单个数据的时候不能加many=True否则报错:TypeError: 'Project_Mo' object is not iterable
        return JsonResponse(one.data,json_dumps_params={"ensure_ascii": False},safe=False)

    def post(self,request):
        da = {}
        Cr_data = json.loads(request.body)#将数据转换为字典格式,获取请求之后发送的json数据
        res = ProjectModelSerializer(data=Cr_data)
        try:
            res.is_valid(raise_exception=True)
        except Exception as e:
            da['msg'] = '参数有误'
            da.update(res.errors)
            return JsonResponse(da,status=400,safe=False)
        res.save()#使用序列化器对象.save()可以自动调用序列化器类中的create方法
        return JsonResponse(res.data, status=201)

    def put(self,request,pk=None):
        da={}
        try:
            obj = Project_Mo.objects.get(id=pk)
        except Exception as e:
            da['msg'] = "没有所需要更新的数据，无法更新"
            return JsonResponse(da)
        Cr_data = json.loads(request.body)#将数据转换为字典格式,获取请求之后发送的json数据
        res = ProjectModelSerializer(instance=obj, data=Cr_data)#instance传递的参数为查询出来的参数，data传递的参数为需要更新的参数,必须用sava来保存
        try:
            res.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse(res.errors,status=400)
        res.save()#save方法自动调用update
        return JsonResponse(res.data, status=201)

    def delete(self,request,pk=None):
        res = {}
        try:
            Project_Mo.objects.get(id=pk).delete()
        except Exception as e:
            res['data'] = f'id:{pk}'
            res['msg'] = '数据不存在'
            return JsonResponse(res, status=400)
        res['data'] = f'id:{pk}'
        res['msg'] = '删除数据成功!'
        return JsonResponse(res)

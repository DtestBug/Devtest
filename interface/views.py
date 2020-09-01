from django.shortcuts import render
from django.views import View
from django.http import JsonResponse,HttpResponse,Http404
from .models import Interface_Mo
from .serializers import InterfaceModelSerializer
import json

ret1 = {
    'msg': '参数有误',
    'code': 10001,
}

ret2 = {'msg': '操作成功',
        'code': 10002,
}


class Interface(View):

    def get_object(self,pk):
        try:
            pro_obj = Interface_Mo.objects.get(id=pk)
        except Exception as e:
            raise Http404('哦，我的上帝！您访问的页面飞到九霄云外咯。')
            # return JsonResponse(ret1, json_dumps_params={"ensure_ascii": False}, )
        return pro_obj

    def get(self,request, pk):
        pro_obj = self.get_object(pk)
        one = InterfaceModelSerializer(instance=pro_obj)#查询单个数据的时候不能加many=True否则报错:TypeError: 'Project_Mo' object is not iterable
        return JsonResponse(one.data,json_dumps_params={"ensure_ascii": False},safe=False)


    def post(self,request):
        Cr_data = json.loads(request.body)#将数据转换为字典格式,获取请求之后发送的json数据
        res = InterfaceModelSerializer(data=Cr_data)
        try:

            res.is_valid(raise_exception=True)
        except Exception as e:
            ret1.update(res.errors)
            return JsonResponse(ret1,status=400)
        res.save()#使用序列化器对象.save()可以自动调用序列化器类中的create方法
        return JsonResponse(res.data, status=201)

    def put(self,request, pk):
        pro_obj = self.get_object(pk)
        Cr_data = json.loads(request.body)#将数据转换为字典格式,获取请求之后发送的json数据
        res = InterfaceModelSerializer(instance=pro_obj, data=Cr_data)#instance传递的参数为查询出来的参数，data传递的参数为需要更新的参数,必须用sava来保存
        try:
            res.is_valid(raise_exception=True)
        except Exception as e:
            ret1.update(res.errors)
            return JsonResponse(ret1,status=400)
        res.save()#save方法自动调用update
        return JsonResponse(res.data, status=201)

    def delete(self,request, pk):
        pro_obj = self.get_object(pk)
        pro_obj.delete()
        ret2['data'] = f'id:{pk}'
        return JsonResponse(ret2)


class Interfaces(View):

    # 查询数据库所有数据
    def get(self,request):
        lists = Interface_Mo.objects.all()
        one = InterfaceModelSerializer(instance=lists,many=True)
        return JsonResponse(one.data,json_dumps_params={"ensure_ascii": False},safe=False)



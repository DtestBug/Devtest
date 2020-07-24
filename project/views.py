from django.shortcuts import render
from django.views import View
from django.http import JsonResponse,HttpResponse
from .models import Project_Mo
import json

class Project(View):

    def get(self,request):
        return JsonResponse('GET',json_dumps_params={"ensure_ascii": False})

    def post(self,request):
        res = {}
        Test_data = json.loads(request.body)
        Project_Mo.objects.create(**Test_data)#这里如果改为res['data']=Project_Mo.objects.create(**Test_data)会报错：不是json格式,将变量去掉即可
        res['msg'] = '创建成功'
        res['code'] = 0
        return JsonResponse(res)

    def put(self,request):
        return JsonResponse('GET')

    def delete(self,request):
        return JsonResponse('GET')
